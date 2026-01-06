import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "pizza_project.settings"  # 🔁 change to YOUR project name
)

application = get_wsgi_application()
