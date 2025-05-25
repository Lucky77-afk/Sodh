from setuptools import setup, find_packages

setup(
    name="sodh",
    version="0.1.0",
    packages=find_packages(include=['main', 'main.*']),
    install_requires=[
        'streamlit>=1.0.0',
        'solana>=0.20.0',
        'solders>=0.10.0',
        'base58>=2.0.0',
        'requests>=2.25.0',
    ],
    entry_points={
        'console_scripts': [
            'sodh=main.app:main',
        ],
    },
)
