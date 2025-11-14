import React, { useState, useEffect } from 'react';
import ApiService from '../services/api';

function Workouts() {
  const [personalizedWorkouts, setPersonalizedWorkouts] = useState([]);
  const [allWorkouts, setAllWorkouts] = useState([]);
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');

  useEffect(() => {
    loadWorkouts();
  }, []);

  const loadWorkouts = async () => {
    try {
      const [personalized, all] = await Promise.all([
        ApiService.getPersonalizedWorkouts(),
        ApiService.getWorkoutSuggestions()
      ]);
      setPersonalizedWorkouts(personalized);
      setAllWorkouts(all);
    } catch (error) {
      console.error('Error loading workouts:', error);
    }
  };

  const filteredWorkouts = selectedDifficulty === 'all'
    ? allWorkouts
    : allWorkouts.filter(w => w.difficulty_level === selectedDifficulty);

  const getDifficultyBadgeClass = (difficulty) => {
    switch (difficulty) {
      case 'beginner': return 'bg-success';
      case 'intermediate': return 'bg-warning text-dark';
      case 'advanced': return 'bg-danger';
      default: return 'bg-secondary';
    }
  };

  return (
    <div>
      <h1 className="mb-4">Workout Suggestions</h1>

      {personalizedWorkouts.length > 0 && (
        <div className="card mb-4">
          <div className="card-header bg-primary text-white">
            <h5 className="mb-0">Recommended For You</h5>
          </div>
          <div className="card-body">
            <div className="row">
              {personalizedWorkouts.map((workout) => (
                <div key={workout.id} className="col-md-6 mb-3">
                  <div className="card h-100">
                    <div className="card-body">
                      <div className="d-flex justify-content-between align-items-start mb-2">
                        <h6>{workout.title}</h6>
                        <span className={`badge ${getDifficultyBadgeClass(workout.difficulty_level)}`}>
                          {workout.difficulty_level}
                        </span>
                      </div>
                      <p className="text-muted small">{workout.description}</p>
                      <div className="d-flex justify-content-between align-items-center">
                        <small>
                          <strong>Duration:</strong> {workout.estimated_duration} min
                        </small>
                        <small>
                          <strong>Category:</strong> {workout.category}
                        </small>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      <div className="card">
        <div className="card-header">
          <div className="d-flex justify-content-between align-items-center">
            <h5 className="mb-0">All Workouts</h5>
            <div>
              <label className="me-2">Filter:</label>
              <select
                className="form-select form-select-sm d-inline-block"
                style={{ width: 'auto' }}
                value={selectedDifficulty}
                onChange={(e) => setSelectedDifficulty(e.target.value)}
              >
                <option value="all">All Levels</option>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
          </div>
        </div>
        <div className="card-body">
          {filteredWorkouts.length > 0 ? (
            <div className="row">
              {filteredWorkouts.map((workout) => (
                <div key={workout.id} className="col-md-4 mb-3">
                  <div className="card h-100">
                    <div className="card-body">
                      <div className="d-flex justify-content-between align-items-start mb-2">
                        <h6>{workout.title}</h6>
                        <span className={`badge ${getDifficultyBadgeClass(workout.difficulty_level)}`}>
                          {workout.difficulty_level}
                        </span>
                      </div>
                      <p className="text-muted small">{workout.description}</p>
                      <div className="mb-2">
                        <small><strong>Duration:</strong> {workout.estimated_duration} min</small>
                      </div>
                      <div className="mb-2">
                        <small><strong>Category:</strong> {workout.category}</small>
                      </div>
                      {workout.target_muscle_groups && (
                        <div className="mb-2">
                          <small><strong>Target:</strong> {workout.target_muscle_groups}</small>
                        </div>
                      )}
                      {workout.equipment_needed && (
                        <div className="mb-2">
                          <small><strong>Equipment:</strong> {workout.equipment_needed}</small>
                        </div>
                      )}
                      {workout.video_url && (
                        <a
                          href={workout.video_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="btn btn-sm btn-outline-primary mt-2"
                        >
                          Watch Video
                        </a>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-muted">No workouts found for this difficulty level.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Workouts;
