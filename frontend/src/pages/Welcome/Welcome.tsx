import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Welcome.css'; // Add CSS for styling

const Welcome: React.FC = () => {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('loginTime');
    navigate('/login');
  };

  return (
    <div className="welcome-container">
      <header className="welcome-header">
        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </header>
      <main className="welcome-content">
        <h1>Welcome, {user.username}!</h1>
      </main>
    </div>
  );
};

export default Welcome;
