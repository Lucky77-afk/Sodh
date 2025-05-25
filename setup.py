from setuptools import setup, find_packages

setup(
    name="sodh",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'streamlit>=1.22.0',
        'solana>=0.30.0',
        'base58>=2.1.1',
        'requests>=2.28.1',
        'python-dotenv>=0.21.0',
    ],
    python_requires='>=3.8',
)
