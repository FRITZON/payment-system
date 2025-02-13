import uuid
import requests
from requests.auth import HTTPBasicAuth
from .constants import COLLECTION_TOKEN_URL, COLLECTION_PAYMENT_URL
from .exceptions import MTNAuthenticationError, MTNPaymentError
from decouple import Config


class MTNMomoService:
    def __init__(self):
        self.subscription_key = Config("MTN_SUBSCRIPTION_KEY")
        self.api_user = Config("MTN_API_USER")
        self.api_key = Config("MTN_API_KEY")
        self.environment = "sandbox"  # ou "production" en prod

    def get_access_token(self):
        """Obtenir un token d'accès"""
        headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "X-Target-Environment": self.environment,
        }

        try:
            response = requests.post(
                COLLECTION_TOKEN_URL,
                headers=headers,
                auth=HTTPBasicAuth(self.api_user, self.api_key),
            )
            response.raise_for_status()
            return response.json()["access_token"]
        except requests.exceptions.RequestException as e:
            raise MTNAuthenticationError(f"Erreur d'authentification MTN: {str(e)}")

    def request_payment(self, transaction):
        """Initier une demande de paiement"""
        token = self.get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "X-Reference-Id": transaction.reference,
            "X-Target-Environment": self.environment,
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Content-Type": "application/json",
        }

        if transaction.callback_url:
            headers["X-Callback-Url"] = transaction.callback_url

        payload = {
            "amount": str(transaction.amount),
            "currency": "XOF",
            # "externalId": str(transaction.reference),
            "payer": {"partyIdType": "MSISDN", "partyId": transaction.phone_number},
            "payerMessage": "Paiement via ADS",
        }

        try:
            response = requests.post(
                COLLECTION_PAYMENT_URL, headers=headers, json=payload
            )
            response.raise_for_status()

            return transaction.reference

        except requests.exceptions.RequestException as e:
            raise MTNPaymentError(f"Erreur de paiement MTN: {str(e)}")

    def check_payment_status(self, reference):
        token = self.get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "X-Target-Environment": self.environment,
            "Ocp-Apim-Subscription-Key": self.subscription_key,
        }

        try:
            response = requests.get(
                f"{COLLECTION_PAYMENT_URL}/{reference}", headers=headers
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise MTNPaymentError(f"Erreur de vérification du statut: {str(e)}")
