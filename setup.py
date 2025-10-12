#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="v2x-quantum-security",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Comprehensive simulation framework for V2X network security in the quantum computing era",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/v2x-quantum-security",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security :: Cryptography",
        "Topic :: Scientific/Engineering :: Simulation",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "isort>=5.13.0",
            "flake8>=6.0.0",
        ],
        "quantum": [
            "qiskit-aer>=0.12.0",
            "cirq>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "v2x-simulator=src.ui.cli:main",
            "v2x-quantum=src.quantum.quantum_simulator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "v2x_quantum_security": [
            "config/*.json",
            "config/*.yaml",
            "data/scenarios/*.json",
        ],
    },
)
