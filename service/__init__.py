"""
Package: service
Account microservice application package.
"""
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS

from service import config

app = Flask(__name__)
app.config.from_object(config)

# Security headers
# Talisman configures secure HTTP response headers for the service.
talisman = Talisman(app)

# Cross-Origin Resource Sharing policy
cors = CORS(app)

# Import routes after the Flask application is created.
from service import routes  # noqa: E402,F401

# Initialize the database after the application is configured.
from service import models  # noqa: E402
models.init_db(app)
