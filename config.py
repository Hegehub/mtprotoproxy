import os


def _parse_users(raw_users: str):
    users = {}
    for item in raw_users.split(','):
        item = item.strip()
        if not item:
            continue
        if ':' in item:
            name, secret = item.split(':', 1)
        else:
            name, secret = 'tg', item
        users[name.strip() or 'tg'] = secret.strip()
    return users


PORT = int(os.getenv('PORT', '443'))

# name -> secret (32 hex chars)
USERS = _parse_users(
    os.getenv('USERS', 'tg:00000000000000000000000000000001')
)

MODES = {
    # Classic mode, easy to detect
    'classic': os.getenv('MODE_CLASSIC', 'false').lower() == 'true',

    # Makes the proxy harder to detect
    # Can be incompatible with very old clients
    'secure': os.getenv('MODE_SECURE', 'false').lower() == 'true',

    # Makes the proxy even more hard to detect
    # Can be incompatible with old clients
    'tls': os.getenv('MODE_TLS', 'true').lower() == 'true',
}

# The domain for TLS mode, bad clients are proxied there
# Use random existing domain, proxy checks it on start
TLS_DOMAIN = os.getenv('TLS_DOMAIN', 'www.google.com')

# Tag for advertising, obtainable from @MTProxybot
AD_TAG = os.getenv('AD_TAG', '')

# Optional: bootstrap SOCKS5 upstream settings from Webshare API.
# API docs: https://apidocs.webshare.io/
WEBSHARE_API_KEY = os.getenv('WEBSHARE_API_KEY', '')
WEBSHARE_PLAN_ID = os.getenv('WEBSHARE_PLAN_ID', '')
WEBSHARE_MODE = os.getenv('WEBSHARE_MODE', 'direct')
