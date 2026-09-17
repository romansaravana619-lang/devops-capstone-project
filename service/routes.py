"""REST routes for the Account service."""
from flask import abort, jsonify, make_response, request

from service import app
from service.common import status
from service.models import Account, DataValidationError

HEADER_CONTENT_TYPE = "application/json"


@app.errorhandler(DataValidationError)
def handle_data_validation_error(error):
    """Return a 400 response for invalid request data."""
    return jsonify(error=str(error)), status.HTTP_400_BAD_REQUEST


@app.route("/health")
def health():
    """Health endpoint."""
    return jsonify(status="OK"), status.HTTP_200_OK


@app.route("/")
def index():
    """Root endpoint."""
    return jsonify(name="Account REST API Service", version="1.0"), status.HTTP_200_OK


@app.route("/accounts", methods=["POST"])
def create_accounts():
    """Create an account."""
    check_content_type(HEADER_CONTENT_TYPE)
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    return make_response(jsonify(account.serialize()), status.HTTP_201_CREATED, {"Location": "/"})


@app.route("/accounts", methods=["GET"])
def list_all_accounts():
    """List all accounts."""
    return jsonify([account.serialize() for account in Account.all()]), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    """Read an account by id."""
    account = Account.find(account_id)
    if account is None:
        abort(status.HTTP_404_NOT_FOUND)
    return jsonify(account.serialize()), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """Update an account by id."""
    check_content_type(HEADER_CONTENT_TYPE)
    account = Account.find(account_id)
    if account is None:
        abort(status.HTTP_404_NOT_FOUND)
    account.deserialize(request.get_json())
    account.id = account_id
    account.update()
    return jsonify(account.serialize()), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Delete an account by id."""
    account = Account.find(account_id)
    if account is None:
        abort(status.HTTP_404_NOT_FOUND)
    account.delete()
    return "", status.HTTP_204_NO_CONTENT


def check_content_type(media_type):
    """Validate the Content-Type header."""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Content-Type must be {media_type}")
