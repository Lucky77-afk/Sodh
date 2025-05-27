from setuptools import setup, find_packages

setup(
    name="sodh",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.45.1",
    ],
    python_requires=">=3.9",
)
