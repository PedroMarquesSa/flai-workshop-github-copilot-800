import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
    console.log('Leaderboard API URL:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        setLeaderboard(Array.isArray(leaderboardData) ? leaderboardData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching leaderboard:', error);
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
        <p className="mt-3">Loading leaderboard...</p>
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

  const getRankBadge = (index) => {
    if (index === 0) return <span className="badge bg-warning text-dark">🥇 1st</span>;
    if (index === 1) return <span className="badge bg-secondary">🥈 2nd</span>;
    if (index === 2) return <span className="badge bg-danger">🥉 3rd</span>;
    return <span className="badge bg-light text-dark">{index + 1}</span>;
  };

  return (
    <div className="container mt-4 fade-in">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0">
          <i className="bi bi-trophy"></i> Leaderboard
        </h2>
        <span className="badge bg-primary">{leaderboard.length} Competitors</span>
      </div>
      
      <div className="card">
        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-hover mb-0">
              <thead>
                <tr>
                  <th><i className="bi bi-award"></i> Rank</th>
                  <th><i className="bi bi-person"></i> User</th>
                  <th><i className="bi bi-star"></i> Points</th>
                  <th><i className="bi bi-people"></i> Team</th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.length === 0 ? (
                  <tr>
                    <td colSpan="4" className="text-center py-4">
                      <div className="text-muted">
                        <i className="bi bi-inbox" style={{fontSize: '2rem'}}></i>
                        <p className="mt-2">No leaderboard data found</p>
                      </div>
                    </td>
                  </tr>
                ) : (
                  leaderboard.map((entry, index) => (
                    <tr key={entry.id} className={index < 3 ? 'table-active' : ''}>
                      <td>{getRankBadge(index)}</td>
                      <td className="fw-semibold">{entry.user_name || 'N/A'}</td>
                      <td><span className="badge bg-success">{entry.total_calories || 0}</span></td>
                      <td>{entry.team_name || 'N/A'}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Leaderboard;
