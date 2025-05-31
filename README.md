# DAPPR Collaboration Agreement Smart Contract

This Solana smart contract, built with the Anchor framework, facilitates the management of collaboration agreements, milestones, and payments on the Solana blockchain.

## Features

- Create and manage collaboration agreements
- Define project milestones with budgets and due dates
- Handle USDC payments for completed milestones
- Enforce access controls for different participant roles
- Track agreement status and milestone completion
- Emit events for on-chain transparency

## Prerequisites

- [Rust](https://www.rust-lang.org/tools/install)
- [Solana CLI](https://docs.solana.com/cli/install-solana-cli-tools)
- [Anchor](https://project-serum.github.io/anchor/getting-started/installation.html)
- [Node.js](https://nodejs.org/) (for testing)
- [Yarn](https://yarnpkg.com/) or npm

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd dappr-collab
   ```

2. Install dependencies:
   ```bash
   yarn install
   # or
   npm install
   ```

3. Build the program:
   ```bash
   anchor build
   ```

4. Update the program ID in the `Anchor.toml` and `lib.rs` files if necessary.

## Testing

To run the test suite:

```bash
anchor test --skip-local-validator
```

## Smart Contract Overview

### Key Components

1. **Agreement**: The main account that stores collaboration details, participants, and milestones.
2. **Milestone**: Represents a project phase with a budget and status.
3. **Participant**: Represents a collaborator with a specific role and share percentage.
4. **Vault**: Token account holding funds for the agreement.

### Main Functions

- `initialize_agreement`: Creates a new collaboration agreement
- `add_milestone`: Adds a milestone to an existing agreement
- `fund_agreement`: Funds the agreement with USDC
- `complete_milestone`: Marks a milestone as completed
- `approve_milestone`: Approves a completed milestone and releases payment

## Security Considerations

- Always verify the program ID before interacting with the contract
- Ensure proper access controls are in place for all state-modifying functions
- Use the latest version of Anchor and Solana tooling
- Perform thorough testing before deploying to mainnet

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
