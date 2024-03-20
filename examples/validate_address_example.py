from coin_remitter import CoinRemitter

def validate_address():
    # Initialize the CoinRemitter client for Bitcoin
    btc_client = CoinRemitter(
        api_key='your_bitcoin_api_key', 
        password='your_bitcoin_wallet_password', 
        coin="BTC"
    )

    # Validate a Bitcoin address
    address = '1BoatSLRHtKNngkdXEeobR76b53LETtpyT'
    is_valid = btc_client.validate_address(
        address=address
    )
    
    print(f"Address {address} Valid: {is_valid}")

if __name__ == "__main__":
    validate_address()
