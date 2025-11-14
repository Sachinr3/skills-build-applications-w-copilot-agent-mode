# OctoFit Tracker - Quick Start Guide

## Backend (Django API)

### Prerequisites
- Python 3.13+ installed
- MongoDB installed and running
- Virtual environment created

### Start the Django Server

**Option 1: Using the batch file (Easiest)**
```bash
# Double-click start_server.bat
# OR run from command line:
start_server.bat
```

**Option 2: Manual start**
```bash
# Navigate to backend directory
cd octofit-tracker\backend

# Activate virtual environment
venv\Scripts\activate

# Start server
python manage.py runserver
```

The server will start at: **http://127.0.0.1:8000/**

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/` | API root with endpoint list |
| `/api/users/` | User management |
| `/api/users/register/` | User registration |
| `/api/profiles/` | User profiles |
| `/api/activities/` | Activity tracking |
| `/api/teams/` | Team management |
| `/api/leaderboard/users/` | User leaderboard |
| `/api/leaderboard/teams/` | Team leaderboard |
| `/api/workout-suggestions/` | Workout library |
| `/api/user-workouts/` | User workouts |
| `/api/auth/login/` | Login |
| `/api/auth/logout/` | Logout |

### Admin Access
- **URL**: http://127.0.0.1:8000/admin/
- **Username**: `admin`
- **Password**: `admin123`

### Test API

Run the test script to verify all endpoints:
```bash
octofit-tracker\backend\venv\Scripts\python.exe octofit-tracker\test_api.py
```

## Database

- **Database**: MongoDB
- **Database Name**: `octofit_tracker`
- **Host**: localhost
- **Port**: 27017

### View Database
```bash
mongosh
use octofit_tracker
show collections
```

## Troubleshooting

### Server won't start
1. Check if MongoDB is running:
   ```bash
   Get-Service -Name MongoDB
   ```
2. Check if port 8000 is available:
   ```bash
   Get-NetTCPConnection -LocalPort 8000
   ```

### Database errors
1. Ensure MongoDB service is running
2. Check database connection in settings.py

### Import errors
1. Activate virtual environment first
2. Reinstall requirements:
   ```bash
   pip install -r octofit-tracker\backend\requirements.txt
   ```

## Next Steps

1. **Start the server** using start_server.bat
2. **Test the API** at http://127.0.0.1:8000/api/
3. **Install Node.js** to set up the React frontend
4. **Build the frontend** (after Node.js installation)

## Frontend Setup (After Node.js Installation)

```bash
# Create React app
npx create-react-app octofit-tracker/frontend --template cra-template --use-npm

# Install dependencies
npm install bootstrap react-router-dom --prefix octofit-tracker/frontend

# Start frontend
cd octofit-tracker/frontend
npm start
```

Frontend will run at: **http://localhost:3000/**
