
def get_patient_time_series(patient_id: str= None):
    if patient_id == "ALL" or patient_id is None:
        return [
            {"id": "patient1", "points": [{"score": 0.5}, {"score": 0.8}]},
            {"id": "patient2", "points": [{"score": 0.8}, {"score": 0.9}]},
            {"id": "patient3", "points": [{"score": 0.4}, {"score": 0.7}]}
        
        ]
    return [
        {"id": patient_id, "points": [{"score": 0.5}, {"score": 0.8}]}
    ]  