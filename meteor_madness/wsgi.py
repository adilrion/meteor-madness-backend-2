"""
WSGI config for meteor_madness project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meteor_madness.settings')

application = get_wsgi_application()

