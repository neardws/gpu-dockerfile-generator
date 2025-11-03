"""Configuration models for GPU Dockerfile generation."""

from typing import Optional, List, Dict
from pydantic import BaseModel, Field, field_validator


class BaseImageConfig(BaseModel):
    """Base image configuration."""

    registry: str = Field(default="nvcr.io/nvidia", description="Container registry")
    image: str = Field(default="pytorch", description="Base image name")
    tag: str = Field(default="24.02-py3", description="Image tag")

    @property
    def full_image(self) -> str:
        """Get full image name."""
        return f"{self.registry}/{self.image}:{self.tag}"


class SystemConfig(BaseModel):
    """System configuration."""

    ubuntu_version: Optional[str] = Field(default=None, description="Ubuntu version (if applicable)")
    timezone: str = Field(default="Asia/Chongqing", description="Timezone")
    locale: str = Field(default="C.UTF-8", description="Locale setting")
    apt_mirror: Optional[str] = Field(
        default="https://mirrors.tuna.tsinghua.edu.cn/ubuntu/",
        description="APT mirror URL"
    )
    system_packages: List[str] = Field(
        default_factory=lambda: [
            "git",
            "curl",
            "wget",
            "vim",
            "software-properties-common",
            "libgl1-mesa-glx",
            "libsm6",
            "libxrender1",
            "libxext-dev",
            "ffmpeg"
        ],
        description="System packages to install"
    )


class PythonConfig(BaseModel):
    """Python configuration."""

    version: Optional[str] = Field(default=None, description="Python version (system python)")
    pip_version: Optional[str] = Field(default="latest", description="Pip version")
    pip_mirror: str = Field(
        default="https://pypi.tuna.tsinghua.edu.cn/simple",
        description="PyPI mirror URL"
    )
    use_uv: bool = Field(default=False, description="Use uv package manager")
    uv_version: Optional[str] = Field(default="latest", description="UV version")


class CondaConfig(BaseModel):
    """Conda configuration."""

    enabled: bool = Field(default=True, description="Enable Conda installation")
    version: str = Field(default="2024.06-1", description="Anaconda version")
    install_path: str = Field(default="/root/anaconda", description="Conda installation path")
    channels: List[str] = Field(
        default_factory=lambda: ["conda-forge"],
        description="Conda channels"
    )


class MLFrameworkConfig(BaseModel):
    """Machine Learning framework configuration."""

    pytorch_version: Optional[str] = Field(default=None, description="PyTorch version")
    tensorflow_version: Optional[str] = Field(default=None, description="TensorFlow version")
    cuda_version: Optional[str] = Field(default=None, description="CUDA version")
    cudnn_version: Optional[str] = Field(default=None, description="cuDNN version")
    additional_packages: List[str] = Field(
        default_factory=list,
        description="Additional Python packages"
    )


class ProxyConfig(BaseModel):
    """Proxy configuration (Clash)."""

    enabled: bool = Field(default=False, description="Enable proxy setup")
    clash_subscribe_link: Optional[str] = Field(default=None, description="Clash subscription link")
    clash_secret: str = Field(default="123456", description="Clash secret")
    clash_repo: str = Field(
        default="https://github.com/Elegycloud/clash-for-linux-backup.git",
        description="Clash repository URL"
    )


class SSHConfig(BaseModel):
    """SSH configuration."""

    enabled: bool = Field(default=True, description="Enable SSH setup")
    create_ssh_dir: bool = Field(default=True, description="Create .ssh directory")


class GitHubCLIConfig(BaseModel):
    """GitHub CLI configuration."""

    enabled: bool = Field(default=True, description="Enable GitHub CLI installation")


class MetadataConfig(BaseModel):
    """Dockerfile metadata."""

    version: str = Field(default="v1.0", description="Dockerfile version")
    maintainer: str = Field(default="Your Name", description="Maintainer name")
    author: str = Field(default="Your Name", description="Author name")
    vendor: Optional[str] = Field(default=None, description="Vendor information")


class DockerfileConfig(BaseModel):
    """Complete Dockerfile configuration."""

    metadata: MetadataConfig = Field(default_factory=MetadataConfig)
    base_image: BaseImageConfig = Field(default_factory=BaseImageConfig)
    system: SystemConfig = Field(default_factory=SystemConfig)
    python: PythonConfig = Field(default_factory=PythonConfig)
    conda: CondaConfig = Field(default_factory=CondaConfig)
    ml_framework: MLFrameworkConfig = Field(default_factory=MLFrameworkConfig)
    proxy: ProxyConfig = Field(default_factory=ProxyConfig)
    ssh: SSHConfig = Field(default_factory=SSHConfig)
    github_cli: GitHubCLIConfig = Field(default_factory=GitHubCLIConfig)
    working_dir: str = Field(default="/code", description="Working directory")
    custom_commands: List[str] = Field(
        default_factory=list,
        description="Custom RUN commands to add at the end"
    )

    @field_validator("proxy")
    @classmethod
    def validate_proxy(cls, v):
        """Validate proxy configuration."""
        if v.enabled and not v.clash_subscribe_link:
            raise ValueError("clash_subscribe_link is required when proxy is enabled")
        return v

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "metadata": {
                    "version": "v5.3",
                    "maintainer": "Haowen He",
                    "author": "Haowen He",
                    "vendor": "dig.sias.uestc.cn"
                },
                "base_image": {
                    "registry": "nvcr.io/nvidia",
                    "image": "pytorch",
                    "tag": "24.02-py3"
                },
                "conda": {
                    "enabled": True,
                    "version": "2024.06-1"
                },
                "ml_framework": {
                    "pytorch_version": "2.2.0",
                    "cuda_version": "12.3"
                }
            }
        }
