"""Tests for Dockerfile generator."""

import pytest
from pathlib import Path
from src.generator import DockerfileGenerator
from src.config import DockerfileConfig, BaseImageConfig


def test_generator_initialization():
    """Test generator initialization."""
    generator = DockerfileGenerator()
    assert generator.env is not None


def test_generate_basic_dockerfile():
    """Test basic Dockerfile generation."""
    config = DockerfileConfig()
    generator = DockerfileGenerator()

    content = generator.generate(config)

    # Check for key components
    assert "FROM nvcr.io/nvidia/pytorch:24.02-py3" in content
    assert "MAINTAINER" in content
    assert "LABEL" in content
    assert "ENV LANG=" in content
    assert "apt update" in content


def test_generate_with_custom_base():
    """Test generation with custom base image."""
    config = DockerfileConfig(
        base_image=BaseImageConfig(
            registry="docker.io",
            image="nvidia/cuda",
            tag="12.3.0-base-ubuntu22.04"
        )
    )
    generator = DockerfileGenerator()

    content = generator.generate(config)
    assert "FROM docker.io/nvidia/cuda:12.3.0-base-ubuntu22.04" in content


def test_generate_to_file(tmp_path):
    """Test Dockerfile generation to file."""
    config = DockerfileConfig()
    generator = DockerfileGenerator()

    output_path = tmp_path / "Dockerfile"
    result = generator.generate_to_file(config, output_path)

    assert result.exists()
    assert result.read_text().startswith("FROM")


def test_generate_to_file_overwrite(tmp_path):
    """Test file overwrite behavior."""
    config = DockerfileConfig()
    generator = DockerfileGenerator()

    output_path = tmp_path / "Dockerfile"

    # Create first file
    generator.generate_to_file(config, output_path)

    # Should fail without overwrite
    with pytest.raises(FileExistsError):
        generator.generate_to_file(config, output_path, overwrite=False)

    # Should succeed with overwrite
    generator.generate_to_file(config, output_path, overwrite=True)
