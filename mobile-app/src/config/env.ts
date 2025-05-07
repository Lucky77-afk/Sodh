export interface EnvConfig {
  SOLANA_NETWORK: 'mainnet-beta' | 'testnet' | 'devnet';
  SOLANA_RPC_URL: string;
  API_BASE_URL: string;
  API_KEY: string;
  ENABLE_ANALYTICS: boolean;
  ENABLE_CRASH_REPORTING: boolean;
  APP_VERSION: string;
  BUILD_NUMBER: string;
}

const defaultConfig: EnvConfig = {
  SOLANA_NETWORK: 'devnet',
  SOLANA_RPC_URL: 'https://api.devnet.solana.com',
  API_BASE_URL: 'https://api.example.com',
  API_KEY: '',
  ENABLE_ANALYTICS: false,
  ENABLE_CRASH_REPORTING: false,
  APP_VERSION: '1.0.0',
  BUILD_NUMBER: '1',
};

export const getEnvConfig = (): EnvConfig => {
  // In a real app, this would load from .env file
  return defaultConfig;
}; 