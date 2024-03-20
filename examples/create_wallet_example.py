from coin_remitter import CoinRemitter

def create_new_wallet():
    # Initialize the CoinRemitter client for Ethereum
    eth_client = CoinRemitter(
        api_key='your_ethereum_api_key', 
        password='your_ethereum_wallet_password', 
        coin="ETH"
    )

    # Create a new wallet with an optional label
    response = eth_client.create_new_wallet(
        label='My Ethereum Wallet',
        json_response=True
    )
    
    print("New Wallet Created:")
    print(response)

if __name__ == "__main__":
    create_new_wallet()
