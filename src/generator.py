"""Dockerfile generator using Jinja2 templates."""

import os
from pathlib import Path
from typing import Union
from jinja2 import Environment, FileSystemLoader, select_autoescape

from .config import DockerfileConfig


class DockerfileGenerator:
    """Generate Dockerfiles from configuration."""

    def __init__(self):
        """Initialize the generator with template environment."""
        template_dir = Path(__file__).parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate(self, config: DockerfileConfig) -> str:
        """
        Generate Dockerfile content from configuration.

        Args:
            config: Dockerfile configuration

        Returns:
            Generated Dockerfile content as string
        """
        template = self.env.get_template("base.j2")
        content = template.render(config=config)
        return content

    def generate_to_file(
        self,
        config: DockerfileConfig,
        output_path: Union[str, Path],
        overwrite: bool = False
    ) -> Path:
        """
        Generate Dockerfile and save to file.

        Args:
            config: Dockerfile configuration
            output_path: Output file path
            overwrite: Whether to overwrite existing file

        Returns:
            Path to generated file

        Raises:
            FileExistsError: If file exists and overwrite is False
        """
        output_path = Path(output_path)

        if output_path.exists() and not overwrite:
            raise FileExistsError(
                f"File {output_path} already exists. Use overwrite=True to replace it."
            )

        content = self.generate(config)

        # Create parent directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return output_path


def generate_dockerfile(
    config: DockerfileConfig,
    output_path: Union[str, Path, None] = None,
    overwrite: bool = False
) -> Union[str, Path]:
    """
    Convenience function to generate Dockerfile.

    Args:
        config: Dockerfile configuration
        output_path: Optional output file path. If None, returns content as string.
        overwrite: Whether to overwrite existing file

    Returns:
        Generated Dockerfile content (str) or path to file (Path)
    """
    generator = DockerfileGenerator()

    if output_path is None:
        return generator.generate(config)
    else:
        return generator.generate_to_file(config, output_path, overwrite)
