# coin_remitter

![CoinRemitter](https://coinremitter.com/assets/img/logo.png)

[![PyPI version](https://badge.fury.io/py/coin-remitter.svg)](https://badge.fury.io/py/coin-remitter)

The `coin_remitter` Python package provides a straightforward and powerful interface to the CoinRemitter cryptocurrency payment gateway API. Designed for developers who need to integrate cryptocurrency transactions into their applications, this package supports various operations such as creating wallets, validating addresses, withdrawing coins, handling invoices, and more. Whether you're building a cryptocurrency wallet, a payment gateway for an eCommerce site, or any application that requires cryptocurrency transactions, `coin_remitter` offers the tools you need to get the job done efficiently.

## Features

- **Wallet Operations**: Create new wallets and retrieve balances.
- **Address Validation**: Ensure cryptocurrency addresses are valid before transactions.
- **Withdrawals**: Send coins to external addresses.
- **Transaction Management**: Retrieve transaction details by ID or address.
- **Invoicing**: Create and manage invoices for payments.

## Installation

Install `coin_remitter` using pip:

```bash
pip install coin_remitter
```

### Quick Start

To use `coin_remitter`, you first need to obtain an API key and a password from the CoinRemitter dashboard. Once you have these, you can start by creating a client instance for the cryptocurrency you're working with.

```python
from coin_remitter import CoinRemitter

# Initialize the client for Ethereum
eth_client = CoinRemitter(api_key='your_api_key', password='your_wallet_password', coin="ETH")
```

## Examples

Below are various examples demonstrating how to perform common tasks with the `coin_remitter` package.

### Creating a New Wallet

```python
new_wallet_response = eth_client.create_new_wallet(label='MyNewWallet')
print(f'New Wallet Response: {new_wallet_response}')
```

### Validating an Address
```python
is_valid = eth_client.validate_address(address='0xYourEthereumAddress')
print(f'Address Valid: {is_valid}')
```

### Withdrawing Coins

```python
withdrawal_url = eth_client.withdraw(amount=0.1, address='0xExternalEthereumAddress')
print(f'Transaction Explorer URL: {withdrawal_url}')
```

For more examples and detailed usage, refer to the Examples section below.

## Documentation

For comprehensive documentation, including a complete list of functionalities and API endpoints, please refer to the CoinRemitter API Documentation.

## Contributing

Contributions to `coin_remitter` are welcome! Please refer to the contributing guidelines for more information on how to report bugs, suggest enhancements, and submit pull requests.

## License
`coin_remitter` is licensed under the MIT License. See the LICENSE file for more details.

## Links
- [CoinRemitter API Documentation](https://coinremitter.com/docs)
- [CoinRemitter Dashboard](https://coinremitter.com/dashboard)
- [CoinRemitter Website](https://coinremitter.com)