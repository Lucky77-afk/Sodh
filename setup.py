from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="sodh",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        '': ['*.svg', '*.css', '*.html'],  # Include all static files
    },
    entry_points={
        'console_scripts': [
            'sodh=sodh.app:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Sodh - Solana Blockchain Explorer",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sodh",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
