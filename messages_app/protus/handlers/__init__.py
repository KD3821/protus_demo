from protus.handlers import oauth, payment


WEBHOOK_HANDLERS = {
    'oauth-access': oauth.provide_oauth_token,
    'payment-final': payment.finalize_payment,
}
