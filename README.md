# Mini Hospital Management System

A full-stack Hospital Management System with a Django backend, vanilla JavaScript frontend, and a serverless email notification service.

## Features

- **User Authentication**:
  - Doctor Registration & Login (with specialization)
  - Patient Registration & Login (with address)
- **Doctor Dashboard**:
  - Manage availability slots.
  - View upcoming appointments.
- **Patient Dashboard**:
  - View available doctors and slots.
  - Book appointments.
  - Receive email confirmations.
- **Notifications**:
  - Automated email notifications upon booking (powered by Serverless Framework).
  - Google Calendar integration (Mocked).

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Database**: SQLite (Default)
- **Serverless**: AWS Lambda (via Serverless Framework Offline for local dev)
- **Language**: Python 3.9+

## Prerequisites

- Python 3.8+ installed
- Node.js & npm installed (for Serverless)
- Git

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/simmrannn/hospital-management-system.git
cd hospital-management-system
```

### 2. Backend Setup (Django)

Create a virtual environment (optional but recommended):
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

Install dependencies:
```bash
pip install django djangorestframework django-cors-headers requests
```

Run migrations:
```bash
python manage.py migrate
```

Start the server:
```bash
python manage.py runserver
```
The backend will run at `http://127.0.0.1:8000/`.

### 3. Email Service Setup (Serverless)

Navigate to the email service directory:
```bash
cd email-service
```

Install dependencies:
```bash
npm install
```

Start the offline service:
```bash
npx serverless offline
```
The email service will run at `http://localhost:3000`.

## Usage

1.  Open your browser and navigate to `http://127.0.0.1:8000/`.
2.  **Register a Doctor**: Create an account with the "Doctor" role.
3.  **Login as Doctor**: Add your availability slots in the dashboard.
4.  **Register a Patient**: Open an incognito window or logout, then register as a "Patient".
5.  **Book Appointment**: Select the doctor and a time slot to book.
6.  **Check Logs**: Check the terminal running `serverless offline` to see the email simulation logs.

## API Endpoints

- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `GET /api/doctor/list/` - List all doctors
- `POST /api/doctor/availability/` - Add availability (Doctor only)
- `GET /api/patient/slots/` - View available slots
- `POST /api/patient/book-appointment/` - Book an appointment

## License

This project is open source and available under the [MIT License](LICENSE).
