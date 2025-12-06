import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api"

def run_verification():
    print("Starting Verification...")
    
    # 1. Register Doctor
    print("\n1. Registering Doctor...")
    doc_data = {
        "username": "dr_house",
        "email": "house@hospital.com",
        "password": "password123",
        "role": "doctor",
        "specialization": "Diagnostician"
    }
    res = requests.post(f"{BASE_URL}/auth/register/", json=doc_data)
    if res.status_code == 201:
        print("Doctor registered successfully.")
    else:
        print(f"Doctor registration failed: {res.text}")
        return

    # Login Doctor to get token (if needed, but register logs in)
    # For simplicity, we'll assume session auth or just use the fact we are logged in if we use a session.
    # But requests.Session is better.
    
    session_doc = requests.Session()
    res = session_doc.post(f"{BASE_URL}/auth/login/", json={"username": "dr_house", "password": "password123"})
    print("Doctor logged in.")

    # 2. Create Availability
    print("\n2. Creating Availability...")
    avail_data = {
        "start_time": "2025-12-05T10:00:00Z",
        "end_time": "2025-12-05T10:30:00Z"
    }
    # We need to handle CSRF if using session auth, or just disable it for API.
    # DRF usually handles this if we use Token or Session with CSRF exempt.
    # For this script, let's assume we might hit CSRF issues unless we configured it.
    # But we are using DRF, so it should be fine if we use BasicAuth or Token.
    # Let's use the session cookies.
    
    # Actually, DRF SessionAuthentication enforces CSRF.
    # I'll use BasicAuth for simplicity in the script if I can, or just grab the CSRF token.
    csrftoken = session_doc.cookies.get('csrftoken')
    headers = {'X-CSRFToken': csrftoken} if csrftoken else {}
    
    res = session_doc.post(f"{BASE_URL}/doctor/availability/", json=avail_data, headers=headers)
    if res.status_code == 201:
        print("Availability created.")
        slot_id = res.json()['id']
    else:
        print(f"Failed to create availability: {res.text}")
        return

    # 3. Register Patient
    print("\n3. Registering Patient...")
    pat_data = {
        "username": "patient_zero",
        "email": "zero@patient.com",
        "password": "password123",
        "role": "patient",
        "address": "123 Sick St"
    }
    res = requests.post(f"{BASE_URL}/auth/register/", json=pat_data)
    if res.status_code == 201:
        print("Patient registered successfully.")
    else:
        print(f"Patient registration failed: {res.text}")
        return

    session_pat = requests.Session()
    res = session_pat.post(f"{BASE_URL}/auth/login/", json={"username": "patient_zero", "password": "password123"})
    print("Patient logged in.")

    # 4. List Slots
    print("\n4. Listing Slots...")
    res = session_pat.get(f"{BASE_URL}/patient/slots/")
    print(f"Slots found: {len(res.json())}")

    # 5. Book Slot
    print("\n5. Booking Slot...")
    csrftoken = session_pat.cookies.get('csrftoken')
    headers = {'X-CSRFToken': csrftoken} if csrftoken else {}
    
    res = session_pat.post(f"{BASE_URL}/patient/book/{slot_id}/", headers=headers)
    if res.status_code == 201:
        print("Booking successful!")
        print(res.json())
    else:
        print(f"Booking failed: {res.text}")

if __name__ == "__main__":
    run_verification()
