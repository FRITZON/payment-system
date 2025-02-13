class MTNAPIError(Exception):
    """Exception de base pour les erreurs API MTN"""
    pass

class MTNAuthenticationError(MTNAPIError):
    """Erreur d'authentification MTN"""
    pass

class MTNPaymentError(MTNAPIError):
    """Erreur lors du paiement MTN"""
    pass