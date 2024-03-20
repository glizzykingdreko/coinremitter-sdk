from coin_remitter import CoinRemitter

def create_and_get_invoice():
    # Initialize the CoinRemitter client for Litecoin
    ltc_client = CoinRemitter(
        api_key='your_litecoin_api_key', 
        password='your_litecoin_wallet_password', 
        coin="LTC"
    )

    # Create an invoice
    invoice_response = ltc_client.create_invoice(
        amount=100,
        name='Service Payment',
        currency='USD',
        expiry_time=15,
        description='Payment for services rendered',
        json_response=True
    )
    print("Invoice Created:")
    print(invoice_response)

    # Assuming the invoice creation returns an ID, let's fetch the invoice details
    if invoice_response.get('flag') == 1:
        invoice_id = invoice_response.get('data', {}).get('invoice_id')
        invoice_status = ltc_client.get_invoice(invoice_id=invoice_id, json_response=True)
        print(f"Details for Invoice ID {invoice_id}:")
        print(invoice_status)

if __name__ == "__main__":
    create_and_get_invoice()
