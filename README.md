# GPU Dockerfile Generator

A Python CLI tool to generate customized Dockerfiles for GPU server environments. This tool helps you quickly create production-ready Dockerfiles for NVIDIA GPU servers with support for PyTorch, TensorFlow, Conda, and various other configurations.

## Features

- 🚀 **Template-based Generation**: Uses Jinja2 templates for flexible and maintainable Dockerfile generation
- 🎯 **GPU-Optimized**: Built specifically for NVIDIA GPU servers with NGC container support
- 🐍 **Python Ecosystem**: Support for pip, uv, and Conda package managers
- 🤖 **ML Frameworks**: Easy configuration for PyTorch and TensorFlow
- 🌐 **Proxy Support**: Built-in support for Clash proxy configuration
- 🔧 **Highly Configurable**: YAML-based configuration with sensible defaults
- 💻 **Interactive Mode**: CLI wizard for easy configuration
- ✅ **Validation**: Built-in configuration validation

## Installation

### Using pip

```bash
pip install git+https://github.com/neardws/gpu-dockerfile-generator.git
```

### Using uv (recommended)

```bash
uv pip install git+https://github.com/neardws/gpu-dockerfile-generator.git
```

**Note**: If you have a custom PyPI mirror configured (like Tsinghua mirror), you may need to temporarily use the official PyPI:

```bash
UV_DEFAULT_INDEX=https://pypi.org/simple uv pip install git+https://github.com/neardws/gpu-dockerfile-generator.git
```

### From source

```bash
git clone https://github.com/neardws/gpu-dockerfile-generator.git
cd gpu-dockerfile-generator
pip install -e .
```

For detailed installation instructions and troubleshooting, see [INSTALL.md](INSTALL.md).

## Quick Start

### 1. Generate with Default Configuration

```bash
gpu-docker-gen generate
```

This creates a basic `Dockerfile` with default settings.

### 2. Interactive Mode

```bash
gpu-docker-gen generate --interactive
```

The tool will prompt you for configuration options step by step.

### 3. Using Configuration File

First, create a sample configuration:

```bash
gpu-docker-gen init --output my-config.yaml
```

Edit `my-config.yaml` to customize your setup, then generate:

```bash
gpu-docker-gen generate --config my-config.yaml --output Dockerfile
```

## Configuration

### Configuration File Structure

The configuration is organized into several sections:

#### Metadata

```yaml
metadata:
  version: v1.0              # Dockerfile version
  maintainer: Your Name      # Maintainer name
  author: Your Name          # Author name
  vendor: your.domain.com    # Vendor information (optional)
```

#### Base Image

```yaml
base_image:
  registry: nvcr.io/nvidia   # Container registry
  image: pytorch             # Base image (pytorch, tensorflow, etc.)
  tag: 24.02-py3            # Image tag
```

Common NVIDIA NGC images:
- `pytorch:24.02-py3` - PyTorch 2.2 with Python 3.10
- `tensorflow:24.01-tf2-py3` - TensorFlow 2.15 with Python 3.10
- `cuda:12.3.0-cudnn9-devel-ubuntu22.04` - CUDA development image

#### System Configuration

```yaml
system:
  timezone: Asia/Chongqing   # System timezone
  locale: C.UTF-8            # System locale
  apt_mirror: https://mirrors.tuna.tsinghua.edu.cn/ubuntu/  # APT mirror
  system_packages:           # System packages to install
    - git
    - curl
    - wget
    - vim
```

#### Python Configuration

```yaml
python:
  version: null              # Python version (null for base image default)
  pip_version: latest        # Pip version
  pip_mirror: https://pypi.tuna.tsinghua.edu.cn/simple  # PyPI mirror
  use_uv: false             # Use uv package manager
  uv_version: latest        # UV version
```

#### Conda Configuration

```yaml
conda:
  enabled: true              # Enable Conda installation
  version: 2024.06-1        # Anaconda version
  install_path: /root/anaconda  # Installation path
  channels:                  # Conda channels
    - conda-forge
```

#### ML Framework

```yaml
ml_framework:
  pytorch_version: 2.2.0    # PyTorch version (optional)
  tensorflow_version: null   # TensorFlow version (optional)
  cuda_version: 12.3        # CUDA version (optional)
  additional_packages:       # Additional packages
    - numpy
    - pandas
```

#### Proxy Configuration

```yaml
proxy:
  enabled: true              # Enable proxy setup
  clash_subscribe_link: YOUR_LINK  # Clash subscription URL
  clash_secret: '123456'    # Clash API secret
  clash_repo: https://github.com/Elegycloud/clash-for-linux-backup.git
```

#### SSH and GitHub CLI

```yaml
ssh:
  enabled: true              # Setup SSH directory
  create_ssh_dir: true      # Create .ssh directory

github_cli:
  enabled: true              # Install GitHub CLI
```

#### Working Directory and Custom Commands

```yaml
working_dir: /code          # Container working directory
custom_commands:            # Custom RUN commands
  - pip install custom-package
  - echo "Custom setup complete"
```

## Examples

The `examples/` directory contains several pre-configured setups:

### Basic GPU Server

```bash
gpu-docker-gen generate --config examples/basic-config.yaml
```

Minimal configuration with PyTorch and Conda.

### Advanced GPU Server with Proxy

```bash
gpu-docker-gen generate --config examples/advanced-config.yaml
```

Complete setup matching the original example, including proxy configuration.

### TensorFlow GPU Server

```bash
gpu-docker-gen generate --config examples/tensorflow-config.yaml
```

Optimized for TensorFlow workloads with uv package manager.

## CLI Commands

### `generate`

Generate a Dockerfile from configuration.

```bash
gpu-docker-gen generate [OPTIONS]
```

**Options:**
- `--config, -c PATH`: Path to YAML configuration file
- `--output, -o PATH`: Output Dockerfile path (default: Dockerfile)
- `--overwrite`: Overwrite existing Dockerfile
- `--interactive, -i`: Interactive mode with prompts

**Examples:**

```bash
# Generate with default config
gpu-docker-gen generate

# Generate from config file
gpu-docker-gen generate --config my-config.yaml

# Interactive mode
gpu-docker-gen generate --interactive

# Custom output path
gpu-docker-gen generate --config my-config.yaml --output docker/Dockerfile
```

### `init`

Create a sample configuration file.

```bash
gpu-docker-gen init [OPTIONS]
```

**Options:**
- `--output, -o PATH`: Output configuration file path (default: docker-config.yaml)

**Example:**

```bash
gpu-docker-gen init --output my-config.yaml
```

### `validate`

Validate a configuration file.

```bash
gpu-docker-gen validate CONFIG_FILE
```

**Example:**

```bash
gpu-docker-gen validate my-config.yaml
```

## Use Cases

### 1. Machine Learning Research

Create a GPU server with PyTorch, Jupyter, and common ML libraries:

```yaml
base_image:
  image: pytorch
  tag: 24.02-py3

conda:
  enabled: true

ml_framework:
  additional_packages:
    - jupyter
    - matplotlib
    - scikit-learn
    - pandas
```

### 2. Deep Learning Training

Setup for distributed training with multiple GPUs:

```yaml
base_image:
  image: pytorch
  tag: 24.02-py3

system_packages:
  - git
  - libopenmpi-dev

custom_commands:
  - pip install horovod
  - pip install tensorboard
```

### 3. Development Environment

Complete development setup with tools and proxy:

```yaml
proxy:
  enabled: true
  clash_subscribe_link: YOUR_LINK

github_cli:
  enabled: true

system_packages:
  - git
  - vim
  - tmux
  - htop
```

## Generated Dockerfile Features

The generated Dockerfiles include:

- ✅ NVIDIA NGC base images
- ✅ Multi-stage system package installation
- ✅ Python environment setup with mirrors
- ✅ Conda installation and configuration
- ✅ Timezone configuration
- ✅ APT mirror configuration for faster downloads
- ✅ SSH directory setup
- ✅ Proxy configuration (Clash)
- ✅ GitHub CLI installation
- ✅ Proper labels and metadata
- ✅ Heredoc syntax for cleaner RUN commands

## Development

### Project Structure

```
gpu-dockerfile-generator/
├── src/
│   ├── __init__.py
│   ├── cli.py              # CLI interface
│   ├── config.py           # Configuration models
│   ├── generator.py        # Dockerfile generator
│   └── templates/          # Jinja2 templates
│       ├── base.j2
│       └── components/
│           ├── nvidia_base.j2
│           ├── system_packages.j2
│           ├── python_setup.j2
│           ├── conda_setup.j2
│           ├── proxy_setup.j2
│           ├── ssh_setup.j2
│           └── github_cli.j2
├── examples/               # Example configurations
├── tests/                  # Unit tests
├── pyproject.toml
└── README.md
```

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black src/

# Lint
ruff check src/
```

## Requirements

- Python >= 3.8
- Dependencies:
  - click >= 8.1.0
  - pydantic >= 2.0.0
  - jinja2 >= 3.1.0
  - rich >= 13.0.0
  - pyyaml >= 6.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for the NVIDIA GPU computing community
- Inspired by real-world GPU server deployment needs
- Thanks to the NGC container team for excellent base images

## Support

For issues, questions, or contributions, please open an issue on GitHub:
https://github.com/neardws/gpu-dockerfile-generator/issues

## Author

**Haowen He**
- Email: neardws@gmail.com
- GitHub: [@neardws](https://github.com/neardws)

---

Made with ❤️ for the GPU computing community
