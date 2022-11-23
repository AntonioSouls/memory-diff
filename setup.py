from setuptools import setup
from setuptools import find_packages


setup(
    name="memory_diff",
    version="0.1.0",
    description="Modern MT library to make a difference between two dataset",
    url="#",
    install_requires=[
        "tqdm==4.64.0",
        "boto3==1.17.112",
        "fasttext==0.9.2",
        "scikit-learn==1.1.1",
        "imblearn",
        "pyyaml==5.4.1",
        "sentencepiece==0.1.96",
        "regex==2022.4.24",
        "bleu==0.3",
        "sacrebleu==2.0.0",
        "translate-toolkit==3.5.3",
        "pandas==1.1.5",
        "lxml==4.8.0",
        "Deprecated==1.2.13",
        "docker==5.0.3",
        "mlflow==1.29.0",
        "zipp>=3.1.0",
        "click>=8.0",
    ],
    entry_points={
        "console_scripts": ["cookingbot=cookingbot.cli.main:main"],
    },
    author="Antonio Lanza",
    author_email="antonio.lanza@translated.com",
    packages=find_packages(),
    package_data={"": ["*"]},
    license="MIT",
    zip_safe=False,
)