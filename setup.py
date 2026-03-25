"""Setup configuration for Dharma."""

from setuptools import setup, find_packages

setup(
    name="dharma",
    version="0.1.0",
    description="Interactive developer roadmaps with skill tree progress tracking",
    author="Officethree Technologies",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    extras_require={
        "dev": ["pytest>=7.0"],
    },
)
