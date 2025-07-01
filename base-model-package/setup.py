from setuptools import setup, find_packages

setup(
    name="base-model-package",
    version="0.1.1",
    description="A package for base model, preprocessor, and postprocessor classes.",
    author="Piotr Wachowski",
    author_email="piotr.wachowski@vault51.pl",
    url="https://dev.azure.com/projektarthur/Arthur/_git/base-model-package",
    packages=find_packages(),
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)