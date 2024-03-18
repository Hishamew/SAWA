from setuptools import setup, find_packages

with open("README.md",'r') as f:
    long_description = f.read()
    
setup(
    name = "sawa",
    version = "1.0.0",
    packages = find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.9.0",
)