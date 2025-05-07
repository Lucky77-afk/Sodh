# API Documentation

## Overview

The Sodh Solana Explorer mobile app uses a RESTful API for blockchain data and smart contract interactions. This document outlines the available endpoints, request/response formats, and error handling.

## Base URL

The base URL for all API requests is configured in the environment settings:
```
https://api.example.com
```

## Authentication

All API requests require an API key to be included in the headers:
```
X-API-Key: your_api_key_here
```

## Endpoints

### Blockchain Data

#### Get Account Info
```http
GET /accounts/{address}
```

Response:
```json
{
  "address": "string",
  "balance": "number",
  "owner": "string",
  "executable": "boolean",
  "lamports": "number"
}
```

#### Get Transaction
```http
GET /transactions/{signature}
```

Response:
```json
{
  "signature": "string",
  "slot": "number",
  "blockTime": "number",
  "status": "string",
  "fee": "number",
  "instructions": [
    {
      "programId": "string",
      "accounts": ["string"],
      "data": "string"
    }
  ]
}
```

### Smart Contract Interaction

#### Deploy Contract
```http
POST /contracts/deploy
```

Request:
```json
{
  "programId": "string",
  "data": "string",
  "accounts": ["string"]
}
```

Response:
```json
{
  "signature": "string",
  "status": "string"
}
```

## Error Handling

The API uses standard HTTP status codes and returns error details in the response body:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "object"
  }
}
```

Common error codes:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

## Rate Limiting

API requests are limited to:
- 100 requests per minute for authenticated users
- 10 requests per minute for unauthenticated users

## Retry Mechanism

The API client implements an exponential backoff retry mechanism:
- Maximum 3 retries
- Initial delay of 1 second
- Exponential backoff multiplier of 2

## WebSocket Events

The API also provides WebSocket endpoints for real-time updates:

```javascript
ws://api.example.com/ws/transactions
```

Events:
- `transaction`: New transaction received
- `account`: Account update
- `block`: New block created

## SDK Usage

The API client is available in the `src/utils/api.ts` file:

```typescript
import { apiCall } from '@/utils/api';

// Example usage
const accountInfo = await apiCall<AccountInfo>(`/accounts/${address}`);
```

## Security Considerations

1. Always use HTTPS for API requests
2. Never expose API keys in client-side code
3. Implement proper error handling
4. Use rate limiting to prevent abuse
5. Validate all input data
6. Implement proper authentication and authorization 