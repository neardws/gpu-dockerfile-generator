# Installation Guide

## Method 1: Using pip (Recommended)

```bash
pip install git+https://github.com/neardws/gpu-dockerfile-generator.git
```

## Method 2: Using uv

If you have `uv` configured with a custom PyPI mirror, you may need to temporarily override it:

```bash
UV_DEFAULT_INDEX=https://pypi.org/simple uv pip install git+https://github.com/neardws/gpu-dockerfile-generator.git
```

Or add it to your environment permanently:

```bash
export UV_DEFAULT_INDEX=https://pypi.org/simple
uv pip install git+https://github.com/neardws/gpu-dockerfile-generator.git
```

## Method 3: From Source

```bash
git clone https://github.com/neardws/gpu-dockerfile-generator.git
cd gpu-dockerfile-generator
pip install -e .
```

## Troubleshooting

### Issue: PyPI mirror authentication error

If you see an error like:
```
An index URL (https://pypi.tuna.tsinghua.edu.cn/simple) could not be queried due to a lack of valid authentication credentials (403 Forbidden).
```

**Solution**: Temporarily override the index URL:

For uv:
```bash
UV_DEFAULT_INDEX=https://pypi.org/simple uv pip install git+https://github.com/neardws/gpu-dockerfile-generator.git
```

For pip:
```bash
pip install --index-url https://pypi.org/simple git+https://github.com/neardws/gpu-dockerfile-generator.git
```

### Verify Installation

After installation, test the package works by generating a Dockerfile:

```bash
cd /tmp
python3 -c "
from src.config import DockerfileConfig
from src.generator import DockerfileGenerator

config = DockerfileConfig()
generator = DockerfileGenerator()
content = generator.generate(config)
print('✓ Installation successful!')
print(f'Generated {len(content.split(chr(10)))} lines of Dockerfile')
"
```

You should see:
```
✓ Installation successful!
Generated XX lines of Dockerfile
```

## Quick Start

Once installed, you can use the package in your Python scripts:

```python
from src.config import DockerfileConfig
from src.generator import DockerfileGenerator
import yaml

# Option 1: Use default configuration
config = DockerfileConfig()

# Option 2: Load from YAML file
with open('config.yaml', 'r') as f:
    config_dict = yaml.safe_load(f)
config = DockerfileConfig(**config_dict)

# Generate Dockerfile
generator = DockerfileGenerator()
output_path = generator.generate_to_file(config, 'Dockerfile', overwrite=True)
print(f'Dockerfile generated: {output_path}')
```

## Next Steps

- Check the [examples](examples/) directory for sample configurations
- Read the [README.md](README.md) for detailed usage instructions
- Customize the configuration to match your needs
