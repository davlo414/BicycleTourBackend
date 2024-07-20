# settings.py
import os

# Set DEBUG based on the environment
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
if DEBUG:
    from .dev_settings import *
else:
    from .prod_settings import *