"""Command-line interface for GPU Dockerfile Generator."""

import sys
from pathlib import Path
from typing import Optional
import click
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

from .config import (
    DockerfileConfig,
    BaseImageConfig,
    SystemConfig,
    PythonConfig,
    CondaConfig,
    MLFrameworkConfig,
    ProxyConfig,
    SSHConfig,
    GitHubCLIConfig,
    MetadataConfig,
)
from .generator import DockerfileGenerator

console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="gpu-docker-gen")
def cli():
    """GPU Dockerfile Generator - Generate customized Dockerfiles for GPU servers."""
    pass


@cli.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, path_type=Path),
    help="Path to YAML configuration file",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default="Dockerfile",
    help="Output Dockerfile path (default: Dockerfile)",
)
@click.option(
    "--overwrite",
    is_flag=True,
    help="Overwrite existing Dockerfile",
)
@click.option(
    "--interactive",
    "-i",
    is_flag=True,
    help="Interactive mode - prompts for configuration",
)
def generate(
    config: Optional[Path],
    output: Path,
    overwrite: bool,
    interactive: bool,
):
    """Generate a Dockerfile from configuration."""
    try:
        if interactive:
            dockerfile_config = interactive_config()
        elif config:
            dockerfile_config = load_config_from_file(config)
        else:
            console.print(
                "[yellow]No configuration provided. Using default configuration.[/yellow]"
            )
            dockerfile_config = DockerfileConfig()

        # Generate Dockerfile
        generator = DockerfileGenerator()
        output_path = generator.generate_to_file(dockerfile_config, output, overwrite)

        console.print(
            Panel.fit(
                f"[green]✓[/green] Dockerfile generated successfully!\n\n"
                f"Output: [cyan]{output_path.absolute()}[/cyan]",
                title="Success",
                border_style="green",
            )
        )

    except FileExistsError as e:
        console.print(f"[red]Error:[/red] {e}")
        console.print("[yellow]Use --overwrite to replace the existing file.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@cli.command()
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default="docker-config.yaml",
    help="Output configuration file path",
)
def init(output: Path):
    """Create a sample configuration file."""
    config = DockerfileConfig()

    # Convert to dict and save as YAML
    config_dict = config.model_dump()

    with open(output, "w") as f:
        yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)

    console.print(
        Panel.fit(
            f"[green]✓[/green] Sample configuration created!\n\n"
            f"Output: [cyan]{output.absolute()}[/cyan]\n\n"
            f"Edit this file and run:\n"
            f"[cyan]gpu-docker-gen generate --config {output}[/cyan]",
            title="Success",
            border_style="green",
        )
    )


@cli.command()
@click.argument("config_file", type=click.Path(exists=True, path_type=Path))
def validate(config_file: Path):
    """Validate a configuration file."""
    try:
        config = load_config_from_file(config_file)
        console.print(
            Panel.fit(
                "[green]✓[/green] Configuration is valid!",
                title="Validation Success",
                border_style="green",
            )
        )

        # Display configuration summary
        display_config_summary(config)

    except Exception as e:
        console.print(
            Panel.fit(
                f"[red]✗[/red] Configuration validation failed!\n\n{e}",
                title="Validation Error",
                border_style="red",
            )
        )
        sys.exit(1)


def load_config_from_file(config_path: Path) -> DockerfileConfig:
    """Load configuration from YAML file."""
    with open(config_path, "r") as f:
        config_dict = yaml.safe_load(f)

    return DockerfileConfig(**config_dict)


def interactive_config() -> DockerfileConfig:
    """Interactive configuration wizard."""
    console.print(
        Panel.fit(
            "[bold cyan]GPU Dockerfile Generator[/bold cyan]\n\n"
            "Interactive Configuration Wizard",
            border_style="cyan",
        )
    )

    # Metadata
    console.print("\n[bold]1. Metadata[/bold]")
    version = Prompt.ask("Dockerfile version", default="v1.0")
    maintainer = Prompt.ask("Maintainer name", default="Your Name")
    author = Prompt.ask("Author name", default=maintainer)
    vendor = Prompt.ask("Vendor (optional)", default="")

    metadata = MetadataConfig(
        version=version,
        maintainer=maintainer,
        author=author,
        vendor=vendor if vendor else None,
    )

    # Base Image
    console.print("\n[bold]2. Base Image[/bold]")
    registry = Prompt.ask("Container registry", default="nvcr.io/nvidia")
    image = Prompt.ask("Image name", default="pytorch")
    tag = Prompt.ask("Image tag", default="24.02-py3")

    base_image = BaseImageConfig(registry=registry, image=image, tag=tag)

    # System
    console.print("\n[bold]3. System Configuration[/bold]")
    timezone = Prompt.ask("Timezone", default="Asia/Chongqing")

    system = SystemConfig(timezone=timezone)

    # Python
    console.print("\n[bold]4. Python Configuration[/bold]")
    use_uv = Confirm.ask("Use UV package manager?", default=False)

    python = PythonConfig(use_uv=use_uv)

    # Conda
    console.print("\n[bold]5. Conda Configuration[/bold]")
    enable_conda = Confirm.ask("Install Anaconda?", default=True)
    conda_version = "2024.06-1"
    if enable_conda:
        conda_version = Prompt.ask("Anaconda version", default="2024.06-1")

    conda = CondaConfig(enabled=enable_conda, version=conda_version)

    # ML Framework
    console.print("\n[bold]6. ML Framework (optional)[/bold]")
    pytorch_version = Prompt.ask("PyTorch version (leave empty to skip)", default="")
    tensorflow_version = Prompt.ask("TensorFlow version (leave empty to skip)", default="")

    ml_framework = MLFrameworkConfig(
        pytorch_version=pytorch_version if pytorch_version else None,
        tensorflow_version=tensorflow_version if tensorflow_version else None,
    )

    # Proxy
    console.print("\n[bold]7. Proxy Configuration[/bold]")
    enable_proxy = Confirm.ask("Enable proxy (Clash)?", default=False)
    proxy_config = ProxyConfig(enabled=False)
    if enable_proxy:
        clash_link = Prompt.ask("Clash subscription link")
        proxy_config = ProxyConfig(enabled=True, clash_subscribe_link=clash_link)

    # SSH
    console.print("\n[bold]8. SSH Configuration[/bold]")
    enable_ssh = Confirm.ask("Setup SSH directory?", default=True)
    ssh = SSHConfig(enabled=enable_ssh)

    # GitHub CLI
    console.print("\n[bold]9. GitHub CLI[/bold]")
    enable_gh = Confirm.ask("Install GitHub CLI?", default=True)
    github_cli = GitHubCLIConfig(enabled=enable_gh)

    return DockerfileConfig(
        metadata=metadata,
        base_image=base_image,
        system=system,
        python=python,
        conda=conda,
        ml_framework=ml_framework,
        proxy=proxy_config,
        ssh=ssh,
        github_cli=github_cli,
    )


def display_config_summary(config: DockerfileConfig):
    """Display configuration summary in a table."""
    table = Table(title="Configuration Summary", show_header=True, header_style="bold cyan")
    table.add_column("Component", style="cyan")
    table.add_column("Configuration", style="white")

    table.add_row("Base Image", config.base_image.full_image)
    table.add_row("Maintainer", config.metadata.maintainer)
    table.add_row("Version", config.metadata.version)
    table.add_row("Timezone", config.system.timezone)
    table.add_row("Conda", "Enabled" if config.conda.enabled else "Disabled")
    table.add_row("Proxy", "Enabled" if config.proxy.enabled else "Disabled")
    table.add_row("GitHub CLI", "Enabled" if config.github_cli.enabled else "Disabled")

    console.print(table)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
