import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
    console.log('Workouts API URL:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="container mt-4 text-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="mt-3">Loading workouts...</p>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4 fade-in">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0">
          <i className="bi bi-lightning"></i> Workout Suggestions
        </h2>
        <span className="badge bg-primary">{workouts.length} Workouts</span>
      </div>
      
      <div className="row">
        {workouts.length === 0 ? (
          <div className="col-12">
            <div className="card">
              <div className="card-body text-center py-4">
                <div className="text-muted">
                  <i className="bi bi-inbox" style={{fontSize: '2rem'}}></i>
                  <p className="mt-2">No workout suggestions found</p>
                </div>
              </div>
            </div>
          </div>
        ) : (
          workouts.map((workout) => (
            <div key={workout.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100">
                <div className="card-header">
                  <h5 className="mb-0">{workout.name}</h5>
                </div>
                <div className="card-body">
                  <p className="text-muted">{workout.description}</p>
                  <div className="mb-2">
                    <span className="badge bg-info me-2">{workout.activity_type}</span>
                    <span className="badge bg-warning text-dark">{workout.difficulty_level}</span>
                  </div>
                  <div className="d-flex justify-content-between mt-3">
                    <div>
                      <i className="bi bi-clock"></i> {workout.duration} min
                    </div>
                    <div>
                      <i className="bi bi-fire"></i> {workout.calories_estimate} cal
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Workouts;
