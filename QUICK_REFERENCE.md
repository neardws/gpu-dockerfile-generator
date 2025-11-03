# Quick Reference Guide

## Basic Usage

### Python API

```python
from src.config import DockerfileConfig
from src.generator import DockerfileGenerator

# Create configuration
config = DockerfileConfig()

# Generate Dockerfile
generator = DockerfileGenerator()
generator.generate_to_file(config, 'Dockerfile', overwrite=True)
```

### From YAML Configuration

```python
import yaml
from src.config import DockerfileConfig
from src.generator import DockerfileGenerator

# Load configuration
with open('config.yaml', 'r') as f:
    config_dict = yaml.safe_load(f)

config = DockerfileConfig(**config_dict)

# Generate
generator = DockerfileGenerator()
generator.generate_to_file(config, 'Dockerfile', overwrite=True)
```

## Common Configurations

### PyTorch GPU Server

```python
from src.config import DockerfileConfig, BaseImageConfig

config = DockerfileConfig(
    base_image=BaseImageConfig(
        registry="nvcr.io/nvidia",
        image="pytorch",
        tag="24.02-py3"
    ),
    conda={"enabled": True, "version": "2024.06-1"},
)
```

### TensorFlow GPU Server

```python
config = DockerfileConfig(
    base_image=BaseImageConfig(
        registry="nvcr.io/nvidia",
        image="tensorflow",
        tag="24.01-tf2-py3"
    ),
    conda={"enabled": False},
    python={"use_uv": True}
)
```

### With Proxy Configuration

```python
config = DockerfileConfig(
    proxy={
        "enabled": True,
        "clash_subscribe_link": "http://your-clash-url"
    }
)
```

### Custom System Packages

```python
config = DockerfileConfig(
    system={
        "system_packages": [
            "git", "vim", "tmux", "htop",
            "build-essential", "libopenmpi-dev"
        ]
    }
)
```

### Add Custom Commands

```python
config = DockerfileConfig(
    custom_commands=[
        "pip install jupyter",
        "pip install tensorboard",
        "mkdir -p /workspace/data"
    ]
)
```

## Configuration Reference

### Minimal YAML Configuration

```yaml
metadata:
  version: v1.0
  maintainer: Your Name

base_image:
  registry: nvcr.io/nvidia
  image: pytorch
  tag: 24.02-py3
```

### Full YAML Configuration

See [examples/advanced-config.yaml](examples/advanced-config.yaml)

## Tips

1. **Start with examples**: Copy an example config and modify it
   ```bash
   cp examples/basic-config.yaml my-config.yaml
   ```

2. **Validate before generating**:
   ```python
   try:
       config = DockerfileConfig(**config_dict)
       print("✓ Configuration valid")
   except Exception as e:
       print(f"✗ Error: {e}")
   ```

3. **Preview without saving**:
   ```python
   content = generator.generate(config)
   print(content)  # Preview the Dockerfile
   ```

4. **Use overwrite parameter**:
   ```python
   # Safer - fails if file exists
   generator.generate_to_file(config, 'Dockerfile', overwrite=False)

   # Convenience - always overwrites
   generator.generate_to_file(config, 'Dockerfile', overwrite=True)
   ```

## Common Base Images

### NVIDIA NGC PyTorch
- `nvcr.io/nvidia/pytorch:24.02-py3` - PyTorch 2.2, Python 3.10, CUDA 12.3
- `nvcr.io/nvidia/pytorch:23.12-py3` - PyTorch 2.1, Python 3.10, CUDA 12.3

### NVIDIA NGC TensorFlow
- `nvcr.io/nvidia/tensorflow:24.01-tf2-py3` - TensorFlow 2.15, Python 3.10
- `nvcr.io/nvidia/tensorflow:23.12-tf2-py3` - TensorFlow 2.14, Python 3.10

### NVIDIA NGC CUDA
- `nvcr.io/nvidia/cuda:12.3.0-cudnn9-devel-ubuntu22.04`
- `nvcr.io/nvidia/cuda:12.2.0-cudnn8-devel-ubuntu22.04`

## Example Workflows

### 1. Quick Start

```python
from src.config import DockerfileConfig
from src.generator import DockerfileGenerator

config = DockerfileConfig()
generator = DockerfileGenerator()
generator.generate_to_file(config, 'Dockerfile', overwrite=True)
```

### 2. From YAML

```bash
# Create config
cat > config.yaml << EOF
metadata:
  version: v1.0
  maintainer: $(whoami)

base_image:
  image: pytorch
  tag: 24.02-py3
EOF

# Generate
python3 -c "
import yaml
from src.config import DockerfileConfig
from src.generator import DockerfileGenerator

with open('config.yaml') as f:
    config = DockerfileConfig(**yaml.safe_load(f))

generator = DockerfileGenerator()
generator.generate_to_file(config, 'Dockerfile', overwrite=True)
"
```

### 3. Multiple Configurations

```python
configs = {
    'pytorch': DockerfileConfig(
        base_image={'image': 'pytorch', 'tag': '24.02-py3'}
    ),
    'tensorflow': DockerfileConfig(
        base_image={'image': 'tensorflow', 'tag': '24.01-tf2-py3'}
    ),
}

generator = DockerfileGenerator()
for name, config in configs.items():
    generator.generate_to_file(config, f'Dockerfile.{name}', overwrite=True)
```

## Troubleshooting

### Import Error

```python
# Make sure you're in the project directory
import sys
sys.path.insert(0, '/path/to/gpu-dockerfile-generator')
from src.config import DockerfileConfig
```

### Template Not Found

The templates directory must be in the correct location:
```
src/
├── templates/
│   ├── base.j2
│   └── components/
```

### Validation Error

Check your configuration matches the schema:
```python
from pydantic import ValidationError
try:
    config = DockerfileConfig(**config_dict)
except ValidationError as e:
    print(e.json())
```
