"""Setup file for the database package."""
from setuptools import setup, find_namespace_packages

setup(
    name="fruit-casino-db",
    version="0.1.0",
    packages=find_namespace_packages(include=["src.*"]),
    package_dir={"": "."},
    install_requires=[
        "motor>=3.3.2",
        "pymongo>=4.6.1",
        "pydantic>=2.6.1"
    ],
    python_requires=">=3.11"
)
