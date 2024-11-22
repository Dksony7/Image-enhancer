from setuptools import setup, find_packages

setup(
    name="image-enhancer",
    version="1.0.0",
    description="A lightweight library for image enhancement.",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "Flask"
    ],
)
