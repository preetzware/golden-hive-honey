"""
WSGI config for golden_hive project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import dotenv
# Load environment variables from .env
dotenv.load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_hive.settings')

application = get_wsgi_application()
