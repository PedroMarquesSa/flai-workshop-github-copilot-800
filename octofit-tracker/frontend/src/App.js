import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, NavLink } from 'react-router-dom';
import './App.css';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">
              <i className="bi bi-heart-pulse"></i> OctoFit Tracker
            </Link>
            <button 
              className="navbar-toggler" 
              type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#navbarNav" 
              aria-controls="navbarNav" 
              aria-expanded="false" 
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <NavLink 
                    className={({ isActive }) => isActive ? "nav-link active" : "nav-link"} 
                    to="/users"
                  >
                    <i className="bi bi-person-circle"></i> Users
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink 
                    className={({ isActive }) => isActive ? "nav-link active" : "nav-link"} 
                    to="/teams"
                  >
                    <i className="bi bi-people"></i> Teams
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink 
                    className={({ isActive }) => isActive ? "nav-link active" : "nav-link"} 
                    to="/activities"
                  >
                    <i className="bi bi-activity"></i> Activities
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink 
                    className={({ isActive }) => isActive ? "nav-link active" : "nav-link"} 
                    to="/leaderboard"
                  >
                    <i className="bi bi-trophy"></i> Leaderboard
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink 
                    className={({ isActive }) => isActive ? "nav-link active" : "nav-link"} 
                    to="/workouts"
                  >
                    <i className="bi bi-lightning"></i> Workouts
                  </NavLink>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={
            <div className="container mt-4 fade-in welcome-section">
              <div className="row">
                <div className="col-lg-8 mx-auto">
                  <h1 className="display-4 mb-4">
                    <i className="bi bi-heart-pulse"></i> Welcome to OctoFit Tracker
                  </h1>
                  <p className="lead mb-4">
                    Track your fitness activities, compete with your team, and achieve your goals!
                  </p>
                  <div className="row mt-5">
                    <div className="col-md-4 mb-3">
                      <div className="card h-100 text-center">
                        <div className="card-body">
                          <i className="bi bi-person-circle text-primary" style={{fontSize: '3rem'}}></i>
                          <h5 className="card-title mt-3">Users</h5>
                          <p className="card-text">Manage user profiles and track individual progress</p>
                          <Link to="/users" className="btn btn-primary">
                            View Users
                          </Link>
                        </div>
                      </div>
                    </div>
                    <div className="col-md-4 mb-3">
                      <div className="card h-100 text-center">
                        <div className="card-body">
                          <i className="bi bi-people text-info" style={{fontSize: '3rem'}}></i>
                          <h5 className="card-title mt-3">Teams</h5>
                          <p className="card-text">Create and manage teams for collaborative fitness</p>
                          <Link to="/teams" className="btn btn-primary">
                            View Teams
                          </Link>
                        </div>
                      </div>
                    </div>
                    <div className="col-md-4 mb-3">
                      <div className="card h-100 text-center">
                        <div className="card-body">
                          <i className="bi bi-activity text-success" style={{fontSize: '3rem'}}></i>
                          <h5 className="card-title mt-3">Activities</h5>
                          <p className="card-text">Log and track your daily fitness activities</p>
                          <Link to="/activities" className="btn btn-primary">
                            View Activities
                          </Link>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="row mt-3">
                    <div className="col-md-6 mb-3">
                      <div className="card h-100 text-center">
                        <div className="card-body">
                          <i className="bi bi-trophy text-warning" style={{fontSize: '3rem'}}></i>
                          <h5 className="card-title mt-3">Leaderboard</h5>
                          <p className="card-text">Compete and see who's leading the pack</p>
                          <Link to="/leaderboard" className="btn btn-primary">
                            View Leaderboard
                          </Link>
                        </div>
                      </div>
                    </div>
                    <div className="col-md-6 mb-3">
                      <div className="card h-100 text-center">
                        <div className="card-body">
                          <i className="bi bi-lightning text-danger" style={{fontSize: '3rem'}}></i>
                          <h5 className="card-title mt-3">Workouts</h5>
                          <p className="card-text">Get personalized workout suggestions</p>
                          <Link to="/workouts" className="btn btn-primary">
                            View Workouts
                          </Link>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          } />
          <Route path="/users" element={<Users />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/activities" element={<Activities />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/workouts" element={<Workouts />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
