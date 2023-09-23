import os

if os.getenv('ENV') == 'PRODUCTION':
    from .production import *  # noqa: F401, F403
else:
    from .dev import *  # noqa: F401, F403