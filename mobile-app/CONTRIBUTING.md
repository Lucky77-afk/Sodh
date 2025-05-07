# Contributing to Sodh Solana Explorer

Thank you for your interest in contributing to Sodh Solana Explorer! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to keep our community approachable and respectable.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/sodh-solana-explorer.git
   cd sodh-solana-explorer/mobile-app
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

1. Make your changes
2. Run tests:
   ```bash
   npm test
   ```
3. Run linting:
   ```bash
   npm run lint
   ```
4. Run type checking:
   ```bash
   npm run type-check
   ```
5. Commit your changes:
   ```bash
   git commit -m "feat: your feature description"
   ```
6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. Create a Pull Request

## Code Style

- Follow the TypeScript style guide
- Use ESLint and Prettier for code formatting
- Write meaningful commit messages following conventional commits
- Include tests for new features
- Update documentation as needed

## Testing

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Maintain or improve test coverage
- Test on both iOS and Android platforms

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the documentation if needed
3. The PR will be merged once you have the sign-off of at least one other developer
4. Ensure all CI checks pass

## Release Process

1. Version bump in package.json
2. Update CHANGELOG.md
3. Create a new release tag
4. Deploy to stores

## Questions?

Feel free to open an issue for any questions or concerns. 