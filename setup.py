from setuptools import setup

# This is a minimal setup.py that's only needed for editable installs with pip
# The actual package configuration is in pyproject.toml

if __name__ == "__main__":
    setup(
        # These will be overridden by pyproject.toml
        name="sodh",
        version="0.1.0",
        packages=["sodh"],
        python_requires=">=3.8",
    )
