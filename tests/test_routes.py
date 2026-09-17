"""Unit tests for the Account REST service."""
import unittest

from service import app
from service.models import Account, DataValidationError, db


class TestAccountService(unittest.TestCase):
    """Account service tests covering CRUD, security headers and CORS."""

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        with app.app_context():
            db.drop_all()
            db.create_all()
        cls.client = app.test_client()

    def setUp(self):
        with app.app_context():
            Account.query.delete()
            db.session.commit()

    def _create(self):
        payload = {
            "name": "John Doe",
            "email": "john@doe.com",
            "address": "123 Main St.",
            "phone_number": "555-1212",
        }
        response = self.client.post(
            "/accounts",
            json=payload,
            base_url="https://localhost",
        )
        self.assertEqual(response.status_code, 201)
        return response.get_json()

    def test_index(self):
        response = self.client.get("/", base_url="https://localhost")
        self.assertEqual(response.status_code, 200)

    def test_health(self):
        response = self.client.get("/health", base_url="https://localhost")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "OK")

    def test_create(self):
        account = self._create()
        self.assertEqual(account["name"], "John Doe")
        self.assertIn("date_joined", account)

    def test_create_bad_request(self):
        response = self.client.post(
            "/accounts",
            json={"name": "missing fields"},
            base_url="https://localhost",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_unsupported_media_type(self):
        response = self.client.post(
            "/accounts",
            data="not-json",
            content_type="text/plain",
            base_url="https://localhost",
        )
        self.assertEqual(response.status_code, 415)

    def test_list(self):
        self._create()
        response = self.client.get("/accounts", base_url="https://localhost")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_list_empty(self):
        response = self.client.get("/accounts", base_url="https://localhost")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_read(self):
        account = self._create()
        response = self.client.get(
            f"/accounts/{account['id']}",
            base_url="https://localhost",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], account["id"])

    def test_read_not_found(self):
        response = self.client.get("/accounts/999", base_url="https://localhost")
        self.assertEqual(response.status_code, 404)

    def test_update(self):
        account = self._create()
        payload = {
            "name": "Jane Doe",
            "email": "jane@doe.com",
            "address": "456 Main St.",
            "phone_number": "555-3434",
        }
        response = self.client.put(
            f"/accounts/{account['id']}",
            json=payload,
            base_url="https://localhost",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Jane Doe")

    def test_update_not_found(self):
        response = self.client.put(
            "/accounts/999",
            json={
                "name": "Jane Doe",
                "email": "jane@doe.com",
                "address": "456 Main St.",
            },
            base_url="https://localhost",
        )
        self.assertEqual(response.status_code, 404)

    def test_update_bad_request(self):
        account = self._create()
        response = self.client.put(
            f"/accounts/{account['id']}",
            json={"name": "missing fields"},
            base_url="https://localhost",
        )
        self.assertEqual(response.status_code, 400)

    def test_update_unsupported_media_type(self):
        account = self._create()
        response = self.client.put(
            f"/accounts/{account['id']}",
            data="not-json",
            content_type="text/plain",
            base_url="https://localhost",
        )
        self.assertEqual(response.status_code, 415)

    def test_delete(self):
        account = self._create()
        response = self.client.delete(
            f"/accounts/{account['id']}",
            base_url="https://localhost",
        )
        self.assertEqual(response.status_code, 204)
        with app.app_context():
            self.assertIsNone(Account.find(account["id"]))

    def test_delete_not_found(self):
        response = self.client.delete("/accounts/999", base_url="https://localhost")
        self.assertEqual(response.status_code, 404)

    def test_security_headers(self):
        response = self.client.get("/", base_url="https://localhost")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("X-Frame-Options"), "SAMEORIGIN")
        self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertIn("Content-Security-Policy", response.headers)

    def test_cors_policy(self):
        response = self.client.get("/", base_url="https://localhost")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "*")

    def test_model_validation_error(self):
        with self.assertRaises(DataValidationError):
            Account().deserialize(None)


if __name__ == "__main__":
    unittest.main()
