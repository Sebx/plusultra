#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="plusultra",
    version="0.1.0",
    author="plusultra contributors",
    description="Local text classification engine - Python native runtime",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sebx/plusultra",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=[
        "onnxruntime>=1.16.0",
        "transformers>=4.30.0",
        "numpy>=1.21.0",
    ],
    extras_require={
        "gpu": ["onnxruntime-gpu>=1.16.0"],
        "dev": ["pytest>=7.0", "black>=23.0", "mypy>=1.0"],
    },
)
