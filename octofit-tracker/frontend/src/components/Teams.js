import React, { useState, useEffect } from 'react';
import ApiService from '../services/api';

function Teams() {
  const [myTeams, setMyTeams] = useState([]);
  const [availableTeams, setAvailableTeams] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: ''
  });

  useEffect(() => {
    loadTeams();
  }, []);

  const loadTeams = async () => {
    try {
      const [myTeamsData, allTeamsData] = await Promise.all([
        ApiService.getMyTeams(),
        ApiService.getTeams()
      ]);
      setMyTeams(myTeamsData);
      
      // Filter out teams user is already in
      const myTeamIds = myTeamsData.map(t => t.id);
      const available = allTeamsData.filter(t => !myTeamIds.includes(t.id));
      setAvailableTeams(available);
    } catch (error) {
      console.error('Error loading teams:', error);
    }
  };

  const handleCreateTeam = async (e) => {
    e.preventDefault();
    try {
      await ApiService.createTeam(formData);
      setShowForm(false);
      setFormData({ name: '', description: '' });
      loadTeams();
    } catch (error) {
      console.error('Error creating team:', error);
    }
  };

  const handleJoinTeam = async (teamId) => {
    try {
      await ApiService.joinTeam(teamId);
      loadTeams();
    } catch (error) {
      console.error('Error joining team:', error);
    }
  };

  const handleLeaveTeam = async (teamId) => {
    try {
      await ApiService.leaveTeam(teamId);
      loadTeams();
    } catch (error) {
      console.error('Error leaving team:', error);
    }
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Teams</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Create Team'}
        </button>
      </div>

      {showForm && (
        <div className="card mb-4">
          <div className="card-body">
            <h5>Create New Team</h5>
            <form onSubmit={handleCreateTeam}>
              <div className="mb-3">
                <label className="form-label">Team Name</label>
                <input
                  type="text"
                  className="form-control"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Description</label>
                <textarea
                  className="form-control"
                  rows="3"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                />
              </div>
              <button type="submit" className="btn btn-success">Create Team</button>
            </form>
          </div>
        </div>
      )}

      <div className="row">
        <div className="col-md-6">
          <div className="card mb-4">
            <div className="card-header">
              <h5>My Teams</h5>
            </div>
            <div className="card-body">
              {myTeams.length > 0 ? (
                <div className="list-group">
                  {myTeams.map((team) => (
                    <div key={team.id} className="list-group-item">
                      <div className="d-flex justify-content-between align-items-start">
                        <div>
                          <h6 className="mb-1">{team.name}</h6>
                          <p className="mb-1 text-muted small">{team.description}</p>
                          <div>
                            <span className="badge bg-info me-2">{team.member_count} members</span>
                            <span className="badge bg-success">{team.total_points} points</span>
                          </div>
                        </div>
                        <button
                          className="btn btn-sm btn-outline-danger"
                          onClick={() => handleLeaveTeam(team.id)}
                        >
                          Leave
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-muted">You haven't joined any teams yet.</p>
              )}
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card mb-4">
            <div className="card-header">
              <h5>Available Teams</h5>
            </div>
            <div className="card-body">
              {availableTeams.length > 0 ? (
                <div className="list-group">
                  {availableTeams.map((team) => (
                    <div key={team.id} className="list-group-item">
                      <div className="d-flex justify-content-between align-items-start">
                        <div>
                          <h6 className="mb-1">{team.name}</h6>
                          <p className="mb-1 text-muted small">{team.description}</p>
                          <div>
                            <span className="badge bg-info me-2">{team.member_count} members</span>
                            <span className="badge bg-success">{team.total_points} points</span>
                          </div>
                        </div>
                        <button
                          className="btn btn-sm btn-primary"
                          onClick={() => handleJoinTeam(team.id)}
                        >
                          Join
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-muted">No available teams to join.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Teams;
