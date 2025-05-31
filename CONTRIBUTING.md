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
   - A clear and descriptive title
   - A detailed description of the enhancement
   - Why this enhancement would be useful
   - Any alternative solutions or features you've considered

### Your First Code Contribution

Unsure where to begin contributing? You can start by looking through the `good first issue` and `help wanted` issues:

- [Good first issues](https://github.com/Lucky77-afk/Sodh/labels/good%20first%20issue) - issues which should only require a few lines of code
- [Help wanted](https://github.com/Lucky77-afk/Sodh/labels/help%20wanted) - issues which should be a bit more involved

### Pull Requests

1. Fork the repository and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Workflow

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- When only changing documentation, include `[ci skip]` in the commit description

### Code Style Guide

We use the following tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **Flake8** for linting
- **Mypy** for static type checking

Run these before committing:

```bash
black .
isort .
flake8
mypy .
```

### Testing

We use `pytest` for testing. To run the tests:

```bash
pytest
```

## Additional Notes

### Issue and Pull Request Labels

We use the following labels to help us track and manage issues and pull requests:

- `bug` - Something isn't working
- `documentation` - Improvements or additions to documentation
- `duplicate` - This issue or pull request already exists
- `enhancement` - New feature or request
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `invalid` - This doesn't seem right
- `question` - Further information is requested
- `wontfix` - This will not be worked on

## License

By contributing, you agree that your contributions will be licensed under its AGPL-3.0 License.
