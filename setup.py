from setuptools import setup
from setuptools import find_packages



setup(
    name="memory_diff",
    version="0.1.0",
    description="Modern MT library to make a difference between two dataset",
    url="#",
    install_requires=[],
    author="Antonio Lanza",
    author_email="antonio.lanza@translated.com",
    packages=find_packages(),
    package_data={"": ["*"]},
    license="MIT",
    zip_safe=False,
)