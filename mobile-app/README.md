# Sodh Solana Explorer Mobile App

A mobile application for exploring the Solana blockchain, built with React Native and Expo.

## Features

- View-only wallet connection
- Real-time SOL balance tracking
- Transaction history
- Network status monitoring
- Dark mode UI
- Cross-platform support (iOS & Android)

## Prerequisites

- Node.js (v14 or later)
- npm or yarn
- Expo CLI
- iOS Simulator (for iOS development)
- Android Studio (for Android development)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sodh-solana-explorer.git
cd sodh-solana-explorer
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Start the development server:
```bash
npm start
# or
yarn start
```

4. Run on your preferred platform:
- Press `i` for iOS simulator
- Press `a` for Android emulator
- Scan QR code with Expo Go app for physical device

## Project Structure

```
mobile-app/
├── src/
│   ├── components/     # Reusable UI components
│   ├── context/       # React Context providers
│   ├── navigation/    # Navigation configuration
│   ├── screens/       # Screen components
│   ├── services/      # API and blockchain services
│   ├── types/         # TypeScript type definitions
│   └── utils/         # Utility functions
├── assets/           # Images and other static assets
├── docs/            # Documentation
└── tests/           # Test files
```

## Development

### TypeScript

The project uses TypeScript for type safety. Run type checking:

```bash
npm run type-check
# or
yarn type-check
```

### Linting

ESLint is configured for code quality. Run the linter:

```bash
npm run lint
# or
yarn lint
```

### Testing

Jest is used for testing. Run tests:

```bash
npm test
# or
yarn test
```

## Building for Production

### Android

```bash
npm run build:android
# or
yarn build:android
```

### iOS

```bash
npm run build:ios
# or
yarn build:ios
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](../LICENSE) file for details.

## Acknowledgments

- [React Native](https://reactnative.dev/)
- [Expo](https://expo.dev/)
- [Solana Web3.js](https://solana-labs.github.io/solana-web3.js/)
- [React Navigation](https://reactnavigation.org/)
- [React Native Paper](https://callstack.github.io/react-native-paper/)