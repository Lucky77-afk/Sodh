#!/bin/bash

# Exit on error
set -e

echo "===== Building Sodh Solana Explorer Android APK ====="

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  echo "Installing dependencies..."
  npm install
fi

# Make sure expo-cli is installed
if ! command -v expo &> /dev/null; then
  echo "Installing expo-cli..."
  npm install -g expo-cli
fi

# Make sure EAS CLI is installed
if ! command -v eas &> /dev/null; then
  echo "Installing eas-cli..."
  npm install -g eas-cli
fi

# Configure the build for Android
echo "Configuring EAS Build..."
npx eas-cli build:configure

# Create a build profile if it doesn't exist
if [ ! -f "eas.json" ]; then
  echo "Creating eas.json configuration..."
  cat > eas.json << EOF
{
  "cli": {
    "version": ">= 0.60.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal",
      "android": {
        "buildType": "apk"
      }
    },
    "production": {
      "android": {
        "buildType": "app-bundle"
      }
    }
  },
  "submit": {
    "production": {}
  }
}
EOF
fi

# Build the APK for testing (preview build)
echo "Building Android APK (this may take some time)..."
npx eas-cli build --platform android --profile preview --non-interactive

echo "===== Build process completed ====="
echo ""
echo "Your APK will be available for download once the build is complete."
echo "You can check the build status in the Expo dashboard."
echo ""
echo "Next steps for Play Store submission:"
echo "1. Build a production AAB: npx eas-cli build --platform android --profile production"
echo "2. Upload the AAB to the Google Play Console"
echo "3. Fill in the Store Listing information"
echo "4. Complete Content Rating and Pricing & Distribution"
echo "5. Submit for review"
echo ""

# Make the script executable
chmod +x build-android.sh