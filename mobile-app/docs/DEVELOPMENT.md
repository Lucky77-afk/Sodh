# Development Guide

## Getting Started

### Prerequisites

1. Node.js (v14 or newer)
2. npm or yarn
3. Expo CLI
4. Android Studio (for Android development)
5. Xcode (for iOS development, macOS only)
6. Git

### Environment Setup

1. Install Node.js and npm:
   ```bash
   # Using nvm (recommended)
   nvm install 14
   nvm use 14
   ```

2. Install Expo CLI:
   ```bash
   npm install -g expo-cli
   ```

3. Install project dependencies:
   ```bash
   cd mobile-app
   npm install
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Development Workflow

### Running the App

1. Start the development server:
   ```bash
   npm start
   ```

2. Run on Android:
   ```bash
   npm run android
   ```

3. Run on iOS:
   ```bash
   npm run ios
   ```

### Code Style

We use ESLint and Prettier for code formatting. The configuration is in `.eslintrc.js` and `.prettierrc`.

To format your code:
```bash
npm run lint
```

### TypeScript

The project uses TypeScript for type safety. Key points:
- All new files should use `.ts` or `.tsx` extension
- Use proper type definitions
- Avoid using `any` type
- Use interfaces for object shapes
- Use type guards when necessary

### Testing

1. Run unit tests:
   ```bash
   npm test
   ```

2. Run tests with coverage:
   ```bash
   npm test -- --coverage
   ```

3. Run specific test file:
   ```bash
   npm test -- path/to/test.ts
   ```

### Debugging

1. Using React Native Debugger:
   - Install React Native Debugger
   - Start the app in debug mode
   - Connect to the debugger

2. Using Chrome DevTools:
   - Shake the device or press Cmd+D (iOS) or Cmd+M (Android)
   - Select "Debug JS Remotely"

3. Using console.log:
   ```typescript
   console.log('Debug:', variable);
   ```

### Common Issues

1. **Metro Bundler Issues**
   ```bash
   # Clear Metro bundler cache
   npm start -- --reset-cache
   ```

2. **Build Issues**
   ```bash
   # Clean build folders
   rm -rf android/app/build
   rm -rf ios/build
   ```

3. **Dependency Issues**
   ```bash
   # Clear npm cache
   npm cache clean --force
   # Remove node_modules
   rm -rf node_modules
   # Reinstall dependencies
   npm install
   ```

## Best Practices

### Code Organization

1. **Components**
   - Keep components small and focused
   - Use proper prop types
   - Implement proper error handling
   - Add proper documentation

2. **State Management**
   - Use React Context for global state
   - Use local state for component-specific state
   - Implement proper loading states
   - Handle errors gracefully

3. **API Calls**
   - Use the provided API utility
   - Implement proper error handling
   - Use proper loading states
   - Cache responses when appropriate

### Performance

1. **Rendering**
   - Use React.memo for expensive components
   - Implement proper list virtualization
   - Avoid unnecessary re-renders
   - Use proper key props

2. **Images**
   - Optimize images before adding
   - Use proper image formats
   - Implement proper caching
   - Use proper loading states

3. **Network**
   - Implement proper caching
   - Use proper error handling
   - Implement retry mechanisms
   - Use proper loading states

### Security

1. **Data**
   - Never store sensitive data in AsyncStorage
   - Use proper encryption
   - Implement proper authentication
   - Use proper error handling

2. **API**
   - Use HTTPS for all requests
   - Implement proper authentication
   - Use proper error handling
   - Implement proper rate limiting

## Deployment

### Android

1. Build the app:
   ```bash
   npm run build:android
   ```

2. Test the build:
   ```bash
   npm run build:android:preview
   ```

3. Deploy to Play Store:
   ```bash
   npm run build:android:prod
   ```

### iOS

1. Build the app:
   ```bash
   npm run build:ios
   ```

2. Test the build:
   ```bash
   npm run build:ios:preview
   ```

3. Deploy to App Store:
   ```bash
   npm run build:ios:prod
   ```

## Additional Resources

- [React Native Documentation](https://reactnative.dev/docs/getting-started)
- [Expo Documentation](https://docs.expo.dev)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [ESLint Documentation](https://eslint.org/docs/user-guide)
- [Prettier Documentation](https://prettier.io/docs/en/index.html) 