const API_BASE_URL = 'http://127.0.0.1:8000/api';

class ApiService {
  constructor() {
    this.token = localStorage.getItem('token');
  }

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }

  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };
    if (this.token) {
      headers['Authorization'] = `Token ${this.token}`;
    }
    return headers;
  }

  async register(userData) {
    const response = await fetch(`${API_BASE_URL}/users/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });
    return await response.json();
  }

  async login(username, password) {
    const response = await fetch(`${API_BASE_URL}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    if (data.key) {
      this.setToken(data.key);
    }
    return data;
  }

  async logout() {
    try {
      await fetch(`${API_BASE_URL}/auth/logout/`, {
        method: 'POST',
        headers: this.getHeaders(),
      });
    } finally {
      this.setToken(null);
    }
  }

  async getProfile() {
    const response = await fetch(`${API_BASE_URL}/profiles/my_profile/`, {
      headers: this.getHeaders(),
    });
    return await response.json();
  }

  async getActivities() {
    const response = await fetch(`${API_BASE_URL}/activities/`, {
      headers: this.getHeaders(),
    });
    return await response.json();
  }

  async createActivity(activityData) {
    const response = await fetch(`${API_BASE_URL}/activities/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(activityData),
    });
    return await response.json();
  }

  async getTeams() {
    const response = await fetch(`${API_BASE_URL}/teams/`, {
      headers: this.getHeaders(),
    });
    return await response.json();
  }

  async getMyTeams() {
    const response = await fetch(`${API_BASE_URL}/teams/my_teams/`, {
      headers: this.getHeaders(),
    });
    return await response.json();
  }

  async createTeam(teamData) {
    const response = await fetch(`${API_BASE_URL}/teams/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(teamData),
    });
    return await response.json();
  }

  async joinTeam(teamId) {
    const response = await fetch(`${API_BASE_URL}/teams/${teamId}/join/`, {
      method: 'POST',
      headers: this.getHeaders(),
    });
    return await response.json();
  }

  async getUserLeaderboard(limit = 10) {
    const response = await fetch(`${API_BASE_URL}/leaderboard/users/?limit=${limit}`, {
      headers: this.getHeaders(),
    });
    return await response.json();
  }

  async getTeamLeaderboard(limit = 10) {
    const response = await fetch(`${API_BASE_URL}/leaderboard/teams/?limit=${limit}`, {
      headers: this.getHeaders(),
    });
    return await response.json();
  }

  async getWorkoutSuggestions() {
    const response = await fetch(`${API_BASE_URL}/workout-suggestions/`, {
      headers: this.getHeaders(),
    });
    return await response.json();
  }

  async getPersonalizedWorkouts() {
    const response = await fetch(`${API_BASE_URL}/workout-suggestions/personalized/`, {
      headers: this.getHeaders(),
    });
    return await response.json();
  }
}

export default new ApiService();
