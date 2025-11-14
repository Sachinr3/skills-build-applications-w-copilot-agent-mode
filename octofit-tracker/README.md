# OctoFit Tracker - Complete Application Guide

## Overview
OctoFit Tracker is a full-stack fitness tracking application built for Mergington High School. It includes user authentication, activity logging, team management, competitive leaderboards, and personalized workout suggestions.

## Technology Stack

### Backend
- **Django 4.1.7** - Web framework
- **Django REST Framework 3.14.0** - API framework
- **MongoDB 8.2.1** - NoSQL database
- **djongo 1.3.6** - MongoDB connector for Django
- **dj-rest-auth 2.2.6** - Authentication API
- **django-allauth 0.51.0** - User authentication
- **django-cors-headers 4.5.0** - CORS support

### Frontend
- **React** - JavaScript library
- **React Router DOM** - Client-side routing
- **Bootstrap 5** - CSS framework
- **Axios** - HTTP client (via API service)

## Project Structure

```
octofit-tracker/
├── backend/
│   ├── venv/                          # Python virtual environment
│   ├── octofit_tracker/               # Main Django project
│   │   ├── settings.py                # Django configuration
│   │   ├── urls.py                    # API routing
│   │   └── wsgi.py
│   ├── users/                         # User profiles app
│   │   ├── models.py                  # UserProfile model
│   │   ├── serializers.py             # API serializers
│   │   ├── views.py                   # API viewsets
│   │   └── management/commands/       # Custom commands
│   ├── activities/                    # Activity tracking app
│   │   ├── models.py                  # Activity model
│   │   ├── serializers.py
│   │   └── views.py
│   ├── teams/                         # Team management app
│   │   ├── models.py                  # Team & TeamMembership models
│   │   ├── serializers.py
│   │   └── views.py
│   ├── leaderboard/                   # Leaderboard app
│   │   ├── serializers.py
│   │   └── views.py
│   ├── workouts/                      # Workout suggestions app
│   │   ├── models.py                  # WorkoutSuggestion & UserWorkout models
│   │   ├── serializers.py
│   │   └── views.py
│   ├── requirements.txt               # Python dependencies
│   ├── manage.py                      # Django management script
│   └── start_server.bat               # Backend startup script
└── frontend/
    ├── public/                        # Static files
    ├── src/
    │   ├── components/                # React components
    │   │   ├── Navigation.js          # Navigation bar
    │   │   ├── Login.js               # Login form
    │   │   ├── Register.js            # Registration form
    │   │   ├── Dashboard.js           # User dashboard
    │   │   ├── Activities.js          # Activity logging
    │   │   ├── Teams.js               # Team management
    │   │   ├── Leaderboard.js         # Rankings
    │   │   └── Workouts.js            # Workout suggestions
    │   ├── services/
    │   │   └── api.js                 # API service layer
    │   ├── App.js                     # Main React app
    │   └── index.js                   # Entry point
    ├── package.json                   # Node dependencies
    └── start_frontend.bat             # Frontend startup script
```

## Installation & Setup

### Prerequisites
- Python 3.13.2 or higher
- MongoDB 8.2.1 or higher
- Node.js 24.11.0 LTS or higher

### Backend Setup

1. **Create Python virtual environment:**
   ```bash
   cd octofit-tracker/backend
   python -m venv venv
   ```

2. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start MongoDB service:**
   ```bash
   # Windows
   net start MongoDB

   # macOS
   brew services start mongodb-community

   # Linux
   sudo systemctl start mongod
   ```

5. **Run Django migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Django site entry:**
   ```bash
   python manage.py create_site
   ```

7. **Create admin user:**
   ```bash
   python manage.py create_admin
   ```
   - Default credentials: `admin` / `admin123`

8. **Start backend server:**
   ```bash
   python manage.py runserver 8000
   ```
   Or use the batch file: `start_server.bat`

### Frontend Setup

1. **Install Node.js dependencies:**
   ```bash
   cd octofit-tracker/frontend
   npm install
   ```

2. **Start React development server:**
   ```bash
   npm start
   ```
   Or use the batch file: `start_frontend.bat`

The frontend will automatically open at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/registration/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user

### Users
- `GET /api/users/` - List all users
- `POST /api/users/register/` - Register new user (alternative endpoint)
- `GET /api/users/me/` - Get current user details
- `GET /api/users/my_profile/` - Get current user's profile
- `PUT /api/users/update_profile/` - Update current user's profile

### Activities
- `GET /api/activities/` - List user's activities
- `POST /api/activities/` - Log new activity
- `GET /api/activities/{id}/` - Get activity details
- `PUT /api/activities/{id}/` - Update activity
- `DELETE /api/activities/{id}/` - Delete activity

### Teams
- `GET /api/teams/` - List all teams
- `POST /api/teams/` - Create new team
- `GET /api/teams/{id}/` - Get team details
- `POST /api/teams/{id}/join/` - Join a team
- `POST /api/teams/{id}/leave/` - Leave a team
- `GET /api/teams/my_teams/` - Get user's teams

### Leaderboard
- `GET /api/leaderboard/users/` - Get user rankings
- `GET /api/leaderboard/teams/` - Get team rankings

### Workouts
- `GET /api/workout-suggestions/` - List all workout suggestions
- `GET /api/workout-suggestions/personalized/` - Get personalized workouts
- `GET /api/user-workouts/` - List user's workout history
- `POST /api/user-workouts/` - Log completed workout

## Features

### User Management
- User registration and authentication
- User profiles with fitness levels (beginner, intermediate, advanced, athlete)
- Total points tracking

### Activity Tracking
- Log various activity types (running, walking, cycling, swimming, etc.)
- Automatic point calculation based on:
  - Duration (1 point per minute)
  - Distance (5 points per km)
  - Activity type multipliers
- Activity history view

### Team Management
- Create teams with descriptions
- Join and leave teams
- Team leaderboard with total points
- View team members and activities

### Leaderboards
- User rankings by total points
- Team rankings by combined member points
- Display fitness levels and activity counts

### Workout Suggestions
- Personalized workout recommendations based on fitness level
- Browse all workout suggestions
- Filter by difficulty level (beginner, intermediate, advanced)
- Detailed workout information (duration, equipment, target muscles)

## Default Credentials

- **Admin User:**
  - Username: `admin`
  - Password: `admin123`

## Port Configuration

- **Backend API:** `http://127.0.0.1:8000`
- **Frontend:** `http://localhost:3000`
- **MongoDB:** `mongodb://localhost:27017`

## Development Notes

### MongoDB Configuration
- Database: `octofit_tracker`
- Collections are auto-created by Django
- Uses djongo adapter for Django ORM compatibility

### CORS Configuration
- Allows requests from `http://localhost:3000`
- Credentials allowed for authentication

### Authentication
- Token-based authentication using dj-rest-auth
- Tokens stored in localStorage
- Auto-login after registration

### Point System
- Base points: 1 point per minute of activity
- Distance bonus: 5 points per kilometer
- Activity multipliers:
  - Running: 1.5x
  - Cycling: 1.3x
  - Swimming: 1.8x
  - Strength Training: 1.4x
  - Sports: 1.2x

## Testing

### Test API Endpoints
A test script is included: `test_api.py`

Run tests:
```bash
cd octofit-tracker/backend
python test_api.py
```

### Manual Testing
1. Start backend server
2. Start frontend server
3. Register a new user at `http://localhost:3000/register`
4. Login with credentials
5. Test all features through the UI

## Troubleshooting

### Backend Issues

**MongoDB Connection Error:**
- Ensure MongoDB service is running
- Check connection string in `settings.py`

**Import Errors:**
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall requirements: `pip install -r requirements.txt`

**Migration Errors:**
- Delete `db.sqlite3` if it exists
- Delete migration files except `__init__.py`
- Run: `python manage.py makemigrations && python manage.py migrate`

### Frontend Issues

**npm not recognized:**
- Restart terminal after Node.js installation
- Or use full path: `"C:\Program Files\nodejs\npm.cmd"`

**Port 3000 already in use:**
- Kill process: `netstat -ano | findstr :3000`
- Then: `taskkill /PID <PID> /F`

**API calls failing:**
- Ensure backend is running on port 8000
- Check CORS configuration in Django settings
- Verify API base URL in `src/services/api.js`

## Git Repository

Current branch: `build-octofit-app`

### Commit Changes
```bash
git add .
git commit -m "Your message"
git push origin build-octofit-app
```

## Future Enhancements

- [ ] Add activity editing functionality
- [ ] Implement team chat feature
- [ ] Add workout video player
- [ ] Create mobile-responsive design
- [ ] Add data visualization (charts/graphs)
- [ ] Implement push notifications
- [ ] Add social sharing features
- [ ] Create admin dashboard
- [ ] Add export data functionality
- [ ] Implement dark mode

## License

This project is created for educational purposes as part of the Mergington High School fitness initiative.

## Support

For issues or questions:
1. Check this README
2. Review QUICKSTART.md
3. Check console/terminal for error messages
4. Review Django logs in terminal
