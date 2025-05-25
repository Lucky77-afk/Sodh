from setuptools import setup, find_packages
import os

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Get long description from README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Find all package data files
def find_package_data():
    package_data = {}
    for root, dirs, files in os.walk('sodh'):
        root = root.replace('sodh/', '', 1)
        for file in files:
            if file.endswith(('.py', '.json', '.toml', '.md')):
                continue
            if root not in package_data:
                package_data[root] = []
            package_data[root].append(file)
    return package_data

setup(
    name="sodh",
    version="0.1.0",
    packages=find_packages(include=['sodh', 'sodh.*']),
    package_dir={"": "."},
    package_data={
        'sodh': ['**/*.toml', '**/*.json', '**/*.md'],
    },
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'sodh=run:main',
        ],
    },
    author="Lucky77-afk",
    author_email="your.email@example.com",
    description="Sodh - A Streamlit application for Solana blockchain interactions",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Lucky77-afk/Sodh",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
    ],
    keywords='solana blockchain streamlit dashboard',
    project_urls={
        'Bug Reports': 'https://github.com/Lucky77-afk/Sodh/issues',
        'Source': 'https://github.com/Lucky77-afk/Sodh',
    },
)
