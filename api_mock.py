# api_mock.py
def fetch_records():
    return [
        {"id": 1, "title": "Record A", "status": "pending"},
        {"id": 2, "title": "Record B", "status": "pending"},
    ]

def fetch_detail(record_id):
    return {"id": record_id, "content": "Detail text"}

def approve_record(record_id):
    return True
