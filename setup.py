from setuptools import setup, find_packages

with open("README.md",'r') as f:
    long_description = f.read()
    
setup(
    name = "sawa",
    version = "0.0.4",
    packages = find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.11.0",
)