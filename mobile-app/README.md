# Sodh Solana Explorer Mobile App

A comprehensive Solana blockchain explorer and smart contract interaction platform for Android and iOS.

## Features

- Real-time Solana blockchain data exploration
- Secure wallet connection (view-only)
- Transaction history and details
- Smart contract interaction
- Project collaboration management
- SOL and USDT token support
- Modern, dark-themed UI designed for mobile

## Tech Stack

- React Native / Expo
- Solana Web3.js for blockchain interaction
- React Navigation for seamless routing
- React Native Paper for UI components
- AsyncStorage for local data persistence
- TypeScript for type safety

## Getting Started

### Prerequisites

- Node.js (v14 or newer)
- npm or yarn
- Expo CLI (`npm install -g expo-cli`)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/sodh-solana-explorer.git
   cd sodh-solana-explorer/mobile-app
   ```

2. Install dependencies:
   ```
   npm install
   ```
   
3. Start the development server:
   ```
   npm start
   ```

4. Open the app in the Expo Go app on your phone or use an emulator.

## Building for Production

### Android Build

1. Install EAS CLI:
   ```
   npm install -g eas-cli
   ```

2. Configure EAS Build (one-time setup):
   ```
   eas build:configure
   ```

3. Create a build:
   ```
   eas build --platform android
   ```

4. Follow the prompts to set up signing credentials.

### Google Play Store Deployment

1. Set up a Google Play Developer account.

2. Create a new application in the Google Play Console.

3. Prepare store listing materials:
   - App screenshots (various device sizes)
   - App icon (512x512 px)
   - Feature graphic (1024x500 px)
   - Short description (80 characters max)
   - Full description (4000 characters max)
   - Promotional video (optional)

4. Build an AAB (Android App Bundle) for the Play Store:
   ```
   eas build --platform android --profile production
   ```

5. Upload the AAB to the Google Play Console.

6. Configure Store Listing, Content Rating, and Pricing & Distribution.

7. Submit for review.

## App Structure

```
mobile-app/
├── assets/                 # App icons and images
├── src/
│   ├── components/         # Reusable UI components
│   ├── context/            # React context providers
│   ├── navigation/         # Navigation configuration
│   ├── screens/            # App screens
│   ├── services/           # API services
│   └── utils/              # Utility functions
├── App.tsx                 # Main app component
├── app.json                # Expo configuration
└── package.json            # Dependencies and scripts
```

## Solana Network Configuration

By default, the app connects to Solana's Devnet. To change the network:

1. Open `src/services/solana-service.ts`
2. Modify the connection URL to:
   - Mainnet: `clusterApiUrl('mainnet-beta')`
   - Testnet: `clusterApiUrl('testnet')`
   - Devnet: `clusterApiUrl('devnet')`
   - Custom RPC: `new Connection('https://your-rpc-url')`

## Security Considerations

- The app uses view-only wallet connections by default.
- Transaction signing requires explicit user confirmation.
- No private keys are stored in the app.
- All sensitive operations include confirmation dialogs.

## Play Store Requirements

- Privacy Policy URL is required for Play Store submission.
- Content Rating questionnaire must be completed.
- App signing key should be securely stored.
- Test thoroughly on different Android versions and device sizes.

## Custom Wallet Integration

For enhanced security and functionality, you can integrate hardware wallet support:

1. Install additional dependencies:
   ```
   npm install @solana/wallet-adapter-react @solana/wallet-adapter-base @solana/wallet-adapter-wallets
   ```

2. Follow the integration guide in the Solana documentation.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.