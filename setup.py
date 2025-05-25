from setuptools import setup, find_packages
import os
from pathlib import Path

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Get long description from README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Find all package data files
def find_package_data():
    package_data = {}
    for root, dirs, files in os.walk('sodh'):
        relative_path = os.path.relpath(root, 'sodh')

# Get all files from components and utils
extra_files = []
for directory in ['sodh/components', 'sodh/utils']:
    if os.path.exists(directory):
        extra_files.extend(package_files(directory))

setup(
    name="sodh",
    version="0.1.0",
    packages=find_packages(include=['sodh', 'sodh.*']),
    package_dir={'': '.'},
    package_data={
        'sodh': ['*.py', 'components/*', 'utils/*', '*.toml', '*.json'],
    },
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.8',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'sodh=run:main',
        ],
    },
    author="Lucky77-afk",
    author_email="your.email@example.com",
    description="Sodh - A Streamlit application for Solana blockchain interactions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lucky77-afk/Sodh",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    keywords='solana blockchain streamlit dashboard',
    project_urls={
        'Bug Reports': 'https://github.com/Lucky77-afk/Sodh/issues',
        'Source': 'https://github.com/Lucky77-afk/Sodh',
    },
)
