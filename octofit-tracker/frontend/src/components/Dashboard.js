import React, { useState, useEffect } from 'react';
import ApiService from '../services/api';

function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [profileData, activitiesData] = await Promise.all([
        ApiService.getProfile(),
        ApiService.getActivities()
      ]);
      setProfile(profileData);
      setActivities(activitiesData.slice(0, 5)); // Latest 5 activities
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center"><div className="spinner-border"></div></div>;
  }

  return (
    <div>
      <h1>Dashboard</h1>
      
      {profile && (
        <div className="row mb-4">
          <div className="col-md-4 mb-3">
            <div className="card text-center">
              <div className="card-body">
                <h5 className="card-title">Total Points</h5>
                <h2 className="text-primary">{profile.total_points}</h2>
              </div>
            </div>
          </div>
          <div className="col-md-4 mb-3">
            <div className="card text-center">
              <div className="card-body">
                <h5 className="card-title">Fitness Level</h5>
                <h2 className="text-success text-capitalize">{profile.fitness_level}</h2>
              </div>
            </div>
          </div>
          <div className="col-md-4 mb-3">
            <div className="card text-center">
              <div className="card-body">
                <h5 className="card-title">Activities</h5>
                <h2 className="text-info">{activities.length}</h2>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="card">
        <div className="card-header">
          <h5>Recent Activities</h5>
        </div>
        <div className="card-body">
          {activities.length > 0 ? (
            <div className="list-group">
              {activities.map((activity) => (
                <div key={activity.id} className="list-group-item">
                  <div className="d-flex justify-content-between">
                    <strong className="text-capitalize">{activity.activity_type.replace('_', ' ')}</strong>
                    <span className="badge bg-primary">{activity.points_earned} pts</span>
                  </div>
                  <small className="text-muted">
                    {activity.duration} min • {activity.date}
                  </small>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-muted">No activities yet. Start tracking your fitness!</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
