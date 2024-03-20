
from functools import wraps
from typing import Union, Dict, Any, List
from requests import post

class Endpoints:
    """
    A collection of endpoint URLs for the CoinRemitter API.

    Attributes are formatted strings that can be used to construct full endpoint URLs for various API operations.
    Each attribute corresponds to a specific API function, such as creating a new wallet, validating an address,
    withdrawing coins, and more.

    Usage of an attribute should include formatting with a specific coin type where applicable.
    """
    CREATE_NEW_WALLET = "https://coinremitter.com/api/v3/{}/get-new-address"
    VALIDATE_ADDRESS = "https://coinremitter.com/api/v3/{}/validate-address"
    WITHDRAW = "https://coinremitter.com/api/v3/{}/withdraw"
    GET_TRANSACTION = "https://coinremitter.com/api/v3/{}/get-transaction"
    GET_TRANSACTION_BY_ADDRESS = "https://coinremitter.com/api/v3/{}/get-transaction-by-address"
    GET_BALANCE = "https://coinremitter.com/api/v3/{}/get-balance"
    CREATE_INVOICE = "https://coinremitter.com/api/v3/{}/create-invoice"
    GET_INVOICE = "https://coinremitter.com/api/v3/{}/get-invoice"
    GET_FIAT_TO_CRYPTO_RATE = "https://coinremitter.com/api/v3/{}/fiat-to-crypto-rate"

class CoinRemitter:
    """
    A Python client for interacting with the CoinRemitter cryptocurrency payment gateway API.

    This class provides methods to perform operations such as creating wallets, validating addresses, withdrawing coins,
    managing transactions, and more, by communicating with the CoinRemitter API.

    Attributes:
        COIN (str): The coin type for the API operations (e.g., 'BTC', 'LTC').
        api_key (str): The API key obtained from the CoinRemitter dashboard.
        password (str): The password for the wallet on the CoinRemitter dashboard.

    Methods are designed to match the capabilities of the CoinRemitter API, providing an easy-to-use interface for
    Python applications.
    """
    COIN: str

    def __init__(self, api_key: str, password: str, coin: str) -> None:
        """
        Initializes the CoinRemitter client with the necessary authentication details and coin type.

        Args:
            api_key (str): The API key obtained from the CoinRemitter dashboard for authenticating API requests.
            password (str): The password for the wallet on the CoinRemitter dashboard, used for certain operations.
            coin (str): The coin type for the API operations (e.g., 'BTC', 'LTC').
        """
        self.api_key = api_key
        self.password = password
        self.COIN = coin

    def _request(self, url: str, data: dict = None) -> dict:
        """
        Makes a POST request to the specified CoinRemitter API endpoint with the provided data.

        This internal method automatically includes the API key and password in the request data, handling
        the necessary authentication for API operations.

        Args:
            url (str): The formatted URL to which the request is sent. This URL is obtained from the Endpoints class.
            data (dict, optional): The data to be sent in the request. Defaults to None, which sends an empty dictionary.

        Returns:
            dict: The JSON response from the API as a dictionary.
        """
        if data is None:
            data = {}
        # Automatically include 'api_key' and 'password' in every request
        data.update({
            'api_key': self.api_key,
            'password': self.password
        })
        return post(url.format(self.COIN), json=data).json()
    
    @staticmethod
    def handle_response(success_key):
        """
        Decorator factory for handling API responses uniformly across all instance methods.

        This static method returns a decorator that processes the response from the CoinRemitter API,
        extracting specific data based on the success key or handling errors, depending on the 'json_response' flag
        provided to the decorated method.

        Args:
            success_key (str or List[str]): The key(s) to extract from the API response upon success. If a list, it
            treats the response as a list of dictionaries from which to extract a value using the key.

        Returns:
            function: A decorator that wraps instance methods, handling their responses according to the specified success key.
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Extract and remove 'json_response' from kwargs if present
                json_response = kwargs.pop('json_response', True)
                
                # Execute the function
                result = func(*args, **kwargs)
                
                # Handle the response
                if json_response:
                    return result
                if isinstance(result, dict) and result.get('flag') != 1:
                    return False
                if isinstance(success_key, list):
                    return [r[success_key[0]] for r in result.get('data')]
                return result.get(success_key)

            return wrapper
        return decorator

    @handle_response(success_key='address')
    def create_new_wallet(self, label: str = None, **kwargs) -> Union[Dict[str, Any], str]:
        """
        # Create New Wallet
        Generates a new wallet on the CoinRemitter platform. This method can either return the full JSON response containing detailed information about the created wallet or simply the wallet's address, based on the `json_response` argument.

        ## Args:
        - **label** (`str`, optional): A label to assign to the new wallet for easy identification. Providing a label is optional, but it can be useful for managing multiple wallets.
        - **json_response** (`bool`, optional): Controls the output format of this method. If set to `True`, the method returns the complete JSON response from the API. If `False`, only the wallet's address is returned. Defaults to `True`.

        ## Returns:
        - If `json_response` is `True`:
            - **dict**: The full JSON response from the API, including wallet details such as the address, label, and possibly other metadata.
        - If `json_response` is `False`:
            - **str**: The newly created wallet's address.

        Example usage:

        To create a new wallet and get its address:

        ```python
        wallet_address = create_new_wallet(label="My New Wallet", json_response=False)
        print(f"New Wallet Address: {wallet_address}")
        ```

        To create a wallet and retrieve the full JSON response:

        ```python
        wallet_details = create_new_wallet(label="My Other Wallet")
        print(wallet_details)
        ```

        Note: The actual structure of the JSON response and the presence of additional metadata can vary depending on the CoinRemitter API's current implementation.
        """
        url = Endpoints.CREATE_NEW_WALLET
        data = {'label': label}
        return self._request(url, data)
    
    @handle_response(success_key='valid')
    def validate_address(self, address: str, **kwargs) -> Union[Dict[str, Any], bool]:
        """
        # Validate Coin Address
        Checks if a given coin address is valid on the CoinRemitter platform. This method can return either the complete JSON response from the API, which includes detailed validation information, or a simple boolean indicating the validation status, depending on the `json_response` argument.

        ## Args:
        - **address** (`str`): The coin address to be validated. This should be a string representing the address you want to check for validity.
        - **json_response** (`bool`, optional): Controls the output of the method. If set to `True`, the method returns the complete JSON response, which includes details on the validation process. If `False`, it returns a boolean indicating whether the address is valid. Defaults to `True`.

        ## Returns:
        - If `json_response` is `True`:
            - **dict**: The full JSON response containing details about the validation process and the result. This might include additional metadata provided by the CoinRemitter API.
        - If `json_response` is `False`:
            - **bool**: A boolean value indicating the validation status of the address (`True` for valid, `False` for invalid).

        Example usage:

        To validate an address and receive a simple yes/no answer:

        ```python
        is_valid = validate_address(address="1BoatSLRHtKNngkdXEeobR76b53LETtpyT", json_response=False)
        print(f"Address Valid: {is_valid}")
        ```

        To obtain the full JSON response with details of the validation:

        ```python
        validation_details = validate_address(address="1BoatSLRHtKNngkdXEeobR76b53LETtpyT")
        print(validation_details)
        ```

        Note: Replace `"1BoatSLRHtKNngkdXEeobR76b53LETtpyT"` with the actual address you wish to validate. The example address used here is for illustrative purposes only.
        """
        url = Endpoints.VALIDATE_ADDRESS
        data = {'address': address}
        return self._request(url, data)

    @handle_response(success_key='explorer_url')
    def withdraw(self, amount: float, address: str, **kwargs) -> Union[Dict[str, Any], str]:
        """
        # Withdraw Coins
        Initiates a withdrawal of coins to an external address. This method supports returning either the full JSON response from the API, which includes detailed information about the withdrawal process, or just the URL to the transaction on the blockchain explorer, depending on the `json_response` argument.

        ## Args:
        - **amount** (`float`): The amount of coins to be withdrawn. This should be specified as a floating-point number representing the quantity of coins to transfer.
        - **address** (`str`): The external address where the coins will be sent. This must be a valid coin address for the withdrawal to succeed.
        - **json_response** (`bool`, optional): Determines the format of the output. If `True`, the method returns the complete JSON response from the API. If `False`, only the URL to the transaction on the blockchain explorer is returned. Defaults to `True`.

        ## Returns:
        - If `json_response` is `True`:
            - **dict**: The full JSON response, providing detailed information about the withdrawal, including status, transaction ID, and the explorer URL among other data.
        - If `json_response` is `False`:
            - **str**: The URL to view the transaction on a blockchain explorer, allowing easy tracking of the withdrawal's progress.

        Example usage:

        To initiate a withdrawal and get the explorer URL:

        ```python
        explorer_url = withdraw(amount=0.5, address="3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5", json_response=False)
        print(f"Transaction Explorer URL: {explorer_url}")
        ```

        To obtain the full JSON response with detailed transaction information:

        ```python
        withdrawal_details = withdraw(amount=0.5, address="3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5")
        print(withdrawal_details)
        ```

        Note: Ensure that the `amount` and `address` are valid and correspond to the coin type associated with your CoinRemitter wallet. The example address and amount are for illustrative purposes only.
        """
        url = Endpoints.WITHDRAW
        data = {
            'amount': amount,
            'to_address': address,
        }
        return self._request(url, data)
    
    @handle_response(success_key='explorer_url')
    def get_transaction(self, txid: str, **kwargs) -> Union[Dict[str, Any], str]:
        """
        # Get Transaction
        Retrieves details for a specific transaction by its unique ID. Depending on the `json_response` argument, this method can return either the complete JSON response containing detailed information about the transaction or just the URL to view the transaction on a blockchain explorer.

        ## Args:
        - **txid** (`str`): The unique identifier (transaction ID) of the transaction to retrieve. This should be a string representing the transaction ID you wish to query.
        - **json_response** (`bool`, optional): Controls the output format of this method. If set to `True`, the method returns the complete JSON response, which includes details on the transaction. If `False`, only the URL to the transaction on the blockchain explorer is returned. Defaults to `True`.

        ## Returns:
        - If `json_response` is `True`:
            - **dict**: The full JSON response from the API, including transaction details such as amount, sender, receiver, and the explorer URL among other data.
        - If `json_response` is `False`:
            - **str**: The URL to the transaction on a blockchain explorer, facilitating easy tracking of the transaction status.

        Example usage:

        To get the blockchain explorer URL for a transaction:

        ```python
        transaction_url = get_transaction(txid="abc123def456", json_response=False)
        print(f"Transaction Explorer URL: {transaction_url}")
        ```

        To obtain the full JSON response with detailed transaction information:

        ```python
        transaction_details = get_transaction(txid="abc123def456")
        print(transaction_details)
        ```

        Note: The `txid` parameter must be a valid transaction ID for the associated coin type in your CoinRemitter wallet. The example transaction ID used here is for illustrative purposes only.
        """
        url = Endpoints.GET_TRANSACTION
        data = {'id': txid}
        return self._request(url, data)

    @handle_response(success_key=['explorer_url'])
    def get_transaction_by_address(self, address: str, **kwargs) -> Union[Dict[str, Any], List[str]]:
        """
        # Get Transaction by Address
        Retrieves a list of transactions associated with a specific coin address. This method can return either the full JSON response containing detailed information about the transactions or just a list of transaction IDs, depending on the `json_response` argument.

        ## Args:
        - **address** (`str`): The coin address for which to retrieve transactions. This should be a string representing the address you wish to query.
        - **json_response** (`bool`, optional): Controls the output format of this method. If set to `True`, the method returns the complete JSON response, which includes details on the transactions. If `False`, only a list of transaction IDs is returned. Defaults to `True`.

        ## Returns:
        - If `json_response` is `True`:
            - **dict**: The full JSON response from the API, including details of the transactions associated with the specified address.
        - If `json_response` is `False`:
            - **list**: A list of transaction's explorer URLs.

        Example usage:

        To get a list of transaction IDs for a specific address:

        ```python
        transactions = get_transaction_by_address(address="3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5", json_response=False)
        print(f"Transactions: {transactions}")
        ```

        To obtain the full JSON response with detailed transaction information:

        ```python
        transaction_details = get_transaction_by_address(address="3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5")
        print(transaction_details)
        ```

        Note: Ensure that the `address` parameter is valid and corresponds to the coin type associated with your CoinRemitter wallet. The example address used here is for illustrative purposes only.
        """
        url = Endpoints.GET_TRANSACTION_BY_ADDRESS
        data = {'address': address}
        return self._request(url, data)
    
    @handle_response(success_key='balance')
    def get_balance(self, **kwargs) -> Union[Dict[str, Any], float]:
        """
        # Get balance
        Retrieves the balance of the specified coin.

        This method contacts the API to fetch the current balance and can return either the full JSON response or just the balance figure, based on the `json_response` argument.

        ## Args:
        - **json_response** (`bool`): Determines the return type. If `True`, returns the full JSON response. Defaults to `False`.

        ## Returns:
        - If `json_response` is `True`:
            - **dict**: The full JSON response from the API.
        - If `json_response` is `False`:
            - **float**: The balance of the coin.

        Example usage:
        
        ```python
        balance = get_balance()
        if balance:
            print(f"The current balance is {balance}")
        ```
        """
        url = Endpoints.GET_BALANCE
        return self._request(url)

    @handle_response(success_key='url')
    def create_invoice(
        self, 
        amount: float, 
        name: str = None, 
        currency: str = "USD", 
        expiry_time: int = 10, 
        notify_url: str = None, 
        success_url: str = None, 
        fail_url: str = None, 
        description: str = None, 
        custom_data1: str = None, 
        custom_data2: str = None,
        **kwargs
    ) -> Union[Dict[str, Any], str]:
        """
        # Create Invoice
        Creates an invoice with the specified parameters. This method can return either the full JSON response or just the invoice URL, based on the `json_response` keyword argument.

        ## Args:
        - **amount** (`float`): The amount for the invoice.
        - **name** (`str`, optional): The name associated with the invoice.
        - **currency** (`str`, optional): The currency of the invoice. Defaults to `"USD"`.
        - **expiry_time** (`int`, optional): The expiry time of the invoice in minutes. Defaults to `10`.
        - **notify_url** (`str`, optional): The notification URL to call when the invoice status changes.
        - **success_url** (`str`, optional): The URL to redirect the user to upon successful payment.
        - **fail_url** (`str`, optional): The URL to redirect the user to upon failed payment.
        - **description** (`str`, optional): A description for the invoice.
        - **custom_data1** (`str`, optional): Custom data field 1.
        - **custom_data2** (`str`, optional): Custom data field 2.
        - **json_response** (`bool`, optional): Determines the return type. If `True`, returns the full JSON response. Defaults to `True`.

        ## Returns:
        - If `json_response` is `True`:
            - **dict**: The full JSON response from the API.
        - If `json_response` is `False`:
            - **str**: The URL of the created invoice.

        Example usage:
        
        ```python
        invoice_url = create_invoice(
            amount=100.0,
            name="Test Invoice",
            currency="USD",
            expiry_time=15,
            json_response=False
        )
        print(f"Invoice URL: {invoice_url}")
        ```
        """
        url = Endpoints.CREATE_INVOICE
        data = {
            'amount': amount,
            'name': name,
            'currency': currency,
            'expiry_time': expiry_time,
            'notify_url': notify_url,
            'success_url': success_url,
            'fail_url': fail_url,
            'description': description,
            'custom_data1': custom_data1,
            'custom_data2': custom_data2,
        }
        return self._request(url, data)
    
    @handle_response(success_key='status')
    def get_invoice(self, invoice_id: str, **kwargs) -> Union[Dict[str, Any], str]:
        """
        # Get Invoice
        Retrieves details for a specific invoice by its unique ID.

        This method allows fetching the full invoice details or just the status, depending on the `json_response` argument.

        ## Args:
        - **invoice_id** (`str`): The unique identifier of the invoice to retrieve.
        - **json_response** (`bool`, optional): Determines the type of the return value. If `True`, returns the complete JSON response. Defaults to `True`.

        ## Returns:
        - If `json_response` is `True`:
            - **dict**: The full JSON response containing all details of the invoice.
        - If `json_response` is `False`:
            - **str**: The status of the invoice (e.g., "Paid", "Unpaid").

        Example usage:

        ```python
        invoice_details = get_invoice(invoice_id="abc123")
        if invoice_details:
            print(f"Invoice Status: {invoice_details}")
        else:
            print("Invoice not found or error occurred.")
        ```

        Alternatively, to get just the status:

        ```python
        invoice_status = get_invoice(invoice_id="abc123", json_response=False)
        print(f"Invoice Status: {invoice_status}")
        ```
        """
        url = Endpoints.GET_INVOICE
        data = {'invoice_id': invoice_id}
        return self._request(url, data)
