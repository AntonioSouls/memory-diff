from setuptools import setup
from setuptools import find_packages



setup(
    name="memory_diff",
    version="0.1.0",
    description="Modern MT library to make a difference between two dataset",
    url="#",
    install_requires=[
        "tqdm==4.64.0",
        "shutil==1.7.0",
        "psutil==5.9.4",
        "numpy==1.17.4",
        "bs4==0.0.1",
        "storage==0.0.4.3",
        "typing==3.10.0.0",
        "lxml==4.8.0",
    ],
    author="Antonio Lanza",
    author_email="antonio.lanza@translated.com",
    packages=find_packages(),
    package_data={"": ["*"]},
    license="MIT",
    zip_safe=False,
)