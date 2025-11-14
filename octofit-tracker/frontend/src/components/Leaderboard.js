import React, { useState, useEffect } from 'react';
import ApiService from '../services/api';

function Leaderboard() {
  const [activeTab, setActiveTab] = useState('users');
  const [userLeaderboard, setUserLeaderboard] = useState([]);
  const [teamLeaderboard, setTeamLeaderboard] = useState([]);

  useEffect(() => {
    loadLeaderboards();
  }, []);

  const loadLeaderboards = async () => {
    try {
      const [usersData, teamsData] = await Promise.all([
        ApiService.getUserLeaderboard(),
        ApiService.getTeamLeaderboard()
      ]);
      setUserLeaderboard(usersData);
      setTeamLeaderboard(teamsData);
    } catch (error) {
      console.error('Error loading leaderboards:', error);
    }
  };

  const getRankBadgeClass = (rank) => {
    if (rank === 1) return 'bg-warning text-dark';
    if (rank === 2) return 'bg-secondary';
    if (rank === 3) return 'bg-danger';
    return 'bg-primary';
  };

  return (
    <div>
      <h1 className="mb-4">Leaderboard</h1>

      <ul className="nav nav-tabs mb-4">
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'users' ? 'active' : ''}`}
            onClick={() => setActiveTab('users')}
          >
            User Rankings
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'teams' ? 'active' : ''}`}
            onClick={() => setActiveTab('teams')}
          >
            Team Rankings
          </button>
        </li>
      </ul>

      {activeTab === 'users' ? (
        <div className="card">
          <div className="card-header">
            <h5>Top Users</h5>
          </div>
          <div className="card-body">
            {userLeaderboard.length > 0 ? (
              <div className="table-responsive">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Rank</th>
                      <th>User</th>
                      <th>Fitness Level</th>
                      <th>Activities</th>
                      <th>Total Points</th>
                    </tr>
                  </thead>
                  <tbody>
                    {userLeaderboard.map((user, index) => (
                      <tr key={user.user__id}>
                        <td>
                          <span className={`badge ${getRankBadgeClass(index + 1)}`}>
                            #{index + 1}
                          </span>
                        </td>
                        <td>
                          <strong>{user.user__username}</strong>
                          {user.user__first_name && ` (${user.user__first_name} ${user.user__last_name})`}
                        </td>
                        <td>
                          <span className="badge bg-info text-capitalize">
                            {user.fitness_level}
                          </span>
                        </td>
                        <td>{user.activity_count}</td>
                        <td>
                          <span className="badge bg-success fs-6">
                            {user.total_points}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-muted">No users on the leaderboard yet.</p>
            )}
          </div>
        </div>
      ) : (
        <div className="card">
          <div className="card-header">
            <h5>Top Teams</h5>
          </div>
          <div className="card-body">
            {teamLeaderboard.length > 0 ? (
              <div className="table-responsive">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Rank</th>
                      <th>Team</th>
                      <th>Members</th>
                      <th>Total Points</th>
                    </tr>
                  </thead>
                  <tbody>
                    {teamLeaderboard.map((team, index) => (
                      <tr key={team.id}>
                        <td>
                          <span className={`badge ${getRankBadgeClass(index + 1)}`}>
                            #{index + 1}
                          </span>
                        </td>
                        <td>
                          <div>
                            <strong>{team.name}</strong>
                            {team.description && (
                              <p className="text-muted small mb-0">{team.description}</p>
                            )}
                          </div>
                        </td>
                        <td>
                          <span className="badge bg-info">
                            {team.member_count}
                          </span>
                        </td>
                        <td>
                          <span className="badge bg-success fs-6">
                            {team.total_points}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-muted">No teams on the leaderboard yet.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default Leaderboard;
