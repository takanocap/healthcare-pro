#TORUN: python -m unittest apicode/UnitTests/tests_main.py

import unittest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from apicode.main import app, get_db
from apicode import models, schemas
from uuid import uuid4

client = TestClient(app)

def override_get_db():
    db = MagicMock()
    try:
        yield db
    finally:
        pass

app.dependency_overrides[get_db] = override_get_db

class TestMainEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = client

    @patch("apicode.main.get_db", new=override_get_db)
    def test_login_patient_success(self):
        patient_id = str(uuid4())
        db = next(override_get_db())
        patient = MagicMock()
        patient.patient_id = patient_id
        db.query().filter().first.return_value = patient

        with patch("apicode.main.get_db", return_value=iter([db])):
            response = self.client.post("/login", json={
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1990-01-01"
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"patient_id": patient_id})

    @patch("apicode.main.get_db", new=override_get_db)
    def test_login_patient_invalid(self):
        db = next(override_get_db())
        db.query().filter().first.return_value = None

        with patch("apicode.main.get_db", return_value=iter([db])):
            response = self.client.post("/login", json={
                "first_name": "Jane",
                "last_name": "Smith",
                "date_of_birth": "2000-01-01"
            })
        self.assertEqual(response.status_code, 401)

    @patch("apicode.crud.create_patient")
    def test_create_patient(self, mock_create_patient):
        patient_data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "date_of_birth": "1985-05-05"
        }
        mock_create_patient.return_value = {"patient_id": str(uuid4()), **patient_data}
        response = self.client.post("/patients/", json=patient_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("patient_id", response.json())

    @patch("apicode.crud.get_all_patients")
    def test_get_all_patients(self, mock_get_all_patients):
        mock_get_all_patients.return_value = []
        response = self.client.get("/patients/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    @patch("apicode.crud.get_patient_by_id")
    def test_get_patient_by_id_found(self, mock_get_patient_by_id):
        patient_id = str(uuid4())
        mock_get_patient_by_id.return_value = {"patient_id": patient_id}
        response = self.client.get(f"/patients/{patient_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["patient_id"], patient_id)

    @patch("apicode.crud.get_patient_by_id")
    def test_get_patient_by_id_not_found(self, mock_get_patient_by_id):
        patient_id = str(uuid4())
        mock_get_patient_by_id.return_value = None
        response = self.client.get(f"/patients/{patient_id}")
        self.assertEqual(response.status_code, 404)

    @patch("apicode.crud.create_patient_review")
    def test_create_review(self, mock_create_review):
        review_data = {
            "patient_id": str(uuid4()),
            "review_text": "Great service"
        }
        mock_create_review.return_value = {"review_id": str(uuid4()), **review_data}
        response = self.client.post("/reviews/", json=review_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("review_id", response.json())

    def test_get_review_by_id_found(self):
        review_id = str(uuid4())
        db = next(override_get_db())
        review = MagicMock()
        review.review_id = review_id
        db.query().filter().first.return_value = review

        with patch("apicode.main.get_db", return_value=iter([db])):
            response = self.client.get(f"/reviews/{review_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_review_by_id_not_found(self):
        review_id = str(uuid4())
        db = next(override_get_db())
        db.query().filter().first.return_value = None

        with patch("apicode.main.get_db", return_value=iter([db])):
            response = self.client.get(f"/reviews/{review_id}")
        self.assertEqual(response.status_code, 404)

    @patch("apicode.crud.get_patient_reviews")
    def test_list_reviews(self, mock_get_patient_reviews):
        mock_get_patient_reviews.return_value = []
        response = self.client.get("/reviews/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_review_by_id_for_patient_found(self):
        patient_id = str(uuid4())
        review_id = str(uuid4())
        db = next(override_get_db())
        review = MagicMock()
        review.review_id = review_id
        review.patient_id = patient_id
        db.query().filter().first.return_value = review

        with patch("apicode.main.get_db", return_value=iter([db])):
            response = self.client.get(f"/patients/{patient_id}/reviews/{review_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_review_by_id_for_patient_not_found(self):
        patient_id = str(uuid4())
        review_id = str(uuid4())
        db = next(override_get_db())
        db.query().filter().first.return_value = None

        with patch("apicode.main.get_db", return_value=iter([db])):
            response = self.client.get(f"/patients/{patient_id}/reviews/{review_id}")
        self.assertEqual(response.status_code, 404)

    def test_get_reviews_for_patient_found(self):
        patient_id = str(uuid4())
        db = next(override_get_db())
        patient = MagicMock()
        patient.patient_id = patient_id
        db.query().filter().first.return_value = patient
        db.query().filter().all.return_value = []

        with patch("apicode.main.get_db", return_value=iter([db])):
            response = self.client.get(f"/patients/{patient_id}/reviews")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_reviews_for_patient_not_found(self):
        patient_id = str(uuid4())
        db = next(override_get_db())
        db.query().filter().first.return_value = None

        with patch("apicode.main.get_db", return_value=iter([db])):
            response = self.client.get(f"/patients/{patient_id}/reviews")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()