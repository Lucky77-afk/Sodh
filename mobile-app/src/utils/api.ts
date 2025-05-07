import { getEnvConfig } from '../config/env';

interface ApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  headers?: Record<string, string>;
  body?: any;
  retries?: number;
  retryDelay?: number;
}

const DEFAULT_RETRIES = 3;
const DEFAULT_RETRY_DELAY = 1000;

export class ApiError extends Error {
  constructor(
    public status: number,
    public message: string,
    public data?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export async function apiCall<T>(
  endpoint: string,
  options: ApiOptions = {}
): Promise<T> {
  const {
    method = 'GET',
    headers = {},
    body,
    retries = DEFAULT_RETRIES,
    retryDelay = DEFAULT_RETRY_DELAY,
  } = options;

  const config = getEnvConfig();
  const url = `${config.API_BASE_URL}${endpoint}`;

  const defaultHeaders = {
    'Content-Type': 'application/json',
    'X-API-Key': config.API_KEY,
  };

  let lastError: Error | null = null;

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const response = await fetch(url, {
        method,
        headers: { ...defaultHeaders, ...headers },
        body: body ? JSON.stringify(body) : undefined,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new ApiError(
          response.status,
          errorData?.message || response.statusText,
          errorData
        );
      }

      return await response.json();
    } catch (error) {
      lastError = error as Error;
      
      if (attempt < retries) {
        await delay(retryDelay * Math.pow(2, attempt)); // Exponential backoff
        continue;
      }
      
      throw error;
    }
  }

  throw lastError;
}

// Example usage:
// const data = await apiCall<{ id: number }>('/users', {
//   method: 'POST',
//   body: { name: 'John' },
//   retries: 3,
// }); 