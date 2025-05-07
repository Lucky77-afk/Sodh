declare module '*.png';
declare module '*.jpg';
declare module '*.jpeg';
declare module '*.gif';
declare module '*.svg';

declare module '@env' {
  export const SOLANA_NETWORK: 'mainnet-beta' | 'testnet' | 'devnet';
  export const SOLANA_RPC_URL: string;
  export const API_BASE_URL: string;
  export const API_KEY: string;
  export const ENABLE_ANALYTICS: boolean;
  export const ENABLE_CRASH_REPORTING: boolean;
  export const APP_VERSION: string;
  export const BUILD_NUMBER: string;
}

// Add any other type declarations here 