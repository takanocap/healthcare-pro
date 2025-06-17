# healthcare-pro

curl -X POST http://127.0.0.1:8000/api/v1/companion/respond \
-H "Content-Type: application/json" \
-d '{"message": "I feel tired", "patientId": "abc-123"}'