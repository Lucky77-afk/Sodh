# Contributing to Sodh

Thank you for your interest in contributing to Sodh! We appreciate your time and effort in making this project better.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Reporting Issues](#reporting-issues)
- [Style Guide](#style-guide)
- [License](#license)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before making any contributions.

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** to your local machine:
   ```bash
   git clone https://github.com/your-username/Sodh.git
   cd Sodh
   ```
3. **Set up the development environment** (see below).

## Development Setup

### Prerequisites

- Python 3.10+
- pip (Python package manager)
- Git

### Setup Steps

1. **Set up the virtual environment** (recommended):
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Set up Streamlit secrets**:
   ```bash
   mkdir -p .streamlit
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   # Edit .streamlit/secrets.toml with your API keys
   ```

5. **Run the application**:
   ```bash
   streamlit run run.py
   ```

## Making Changes

1. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/description-of-fix
   ```

2. **Make your changes** following the [style guide](#style-guide).

3. **Run tests** (if available):
   ```bash
   # Run tests
   pytest
   
   # Run with coverage
   pytest --cov=sodh
   ```

4. **Commit your changes** with a descriptive message:
   ```bash
   git add .
   git commit -m "Add feature: brief description of changes"
   ```

## Submitting a Pull Request

1. **Push your changes** to your fork:
   ```bash
   git push origin your-branch-name
   ```

2. **Open a Pull Request** from your fork to the main repository's `main` branch.

3. **Describe your changes** in the PR description:
   - What changes were made
   - Why these changes are necessary
   - Any relevant issue numbers

4. **Request a review** from one of the maintainers.

## Reporting Issues

If you find a bug or have a feature request, please open an issue with the following information:

1. **Bug Report**:
   - A clear and descriptive title
   - Steps to reproduce the issue
   - Expected vs. actual behavior
   - Screenshots if applicable
   - Environment information (OS, Python version, etc.)

2. **Feature Request**:
   - A clear and descriptive title
   - Detailed description of the feature
   - Use cases and benefits
   - Any alternative solutions considered

## Style Guide

### Python Code

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for function signatures
- Keep lines under 88 characters (Black formatter default)
- Use docstrings for all public modules, classes, and functions
- Use Google-style docstrings

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Keep the first line under 50 characters
- Reference issues and pull requests liberally

### Code Review Guidelines

- Be respectful and constructive
- Focus on the code, not the person
- Explain your reasoning
- Suggest improvements rather than just pointing out problems

## License

By contributing to Sodh, you agree that your contributions will be licensed under the GNU Affero General Public License v3.0. See the [LICENSE](LICENSE) file for details.
