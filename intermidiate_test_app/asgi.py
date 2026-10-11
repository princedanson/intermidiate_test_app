"""
ASGI config for intermidiate_test_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os
import sys
from django.core.asgi import get_asgi_application
from pathlib import Path
from fastapi import FastAPI

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intermidiate_test_app.settings')

application = get_asgi_application()

from starlette.applications import Starlette
from starlette.routing import Mount


from dashboard.api.prediction import predict_api as fastapi_app

pre = Starlette(routes=[Mount("/api",app=fastapi_app),
                        Mount("/",app=application),
                        ])
