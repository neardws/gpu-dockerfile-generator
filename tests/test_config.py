"""Tests for configuration models."""

import pytest
from src.config import (
    DockerfileConfig,
    BaseImageConfig,
    ProxyConfig,
)


def test_base_image_full_image():
    """Test base image full name generation."""
    config = BaseImageConfig(
        registry="nvcr.io/nvidia",
        image="pytorch",
        tag="24.02-py3"
    )
    assert config.full_image == "nvcr.io/nvidia/pytorch:24.02-py3"


def test_default_config():
    """Test default configuration."""
    config = DockerfileConfig()
    assert config.working_dir == "/code"
    assert config.system.locale == "C.UTF-8"
    assert config.conda.enabled is True


def test_proxy_validation():
    """Test proxy configuration validation."""
    # Should fail without clash_subscribe_link
    with pytest.raises(ValueError):
        ProxyConfig(enabled=True, clash_subscribe_link=None)

    # Should succeed with link
    proxy = ProxyConfig(enabled=True, clash_subscribe_link="http://example.com")
    assert proxy.enabled is True


def test_custom_commands():
    """Test custom commands."""
    config = DockerfileConfig(
        custom_commands=["echo 'test'", "pip install pytest"]
    )
    assert len(config.custom_commands) == 2
