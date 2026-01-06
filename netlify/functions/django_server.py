import os
from serverless_wsgi import handle_request
from pizza_project.wsgi import application

def handler(event, context):
    # This converts Netlify's request into something Django understands
    return handle_request(application, event, context)