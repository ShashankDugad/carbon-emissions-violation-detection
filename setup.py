from setuptools import setup, find_packages

setup(
    name="carbon-emissions-detection",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyspark>=3.5.1",
        "pandas>=2.2.2",
        "numpy>=1.26.4",
        "requests>=2.31.0",
    ],
    python_requires=">=3.9",
)
