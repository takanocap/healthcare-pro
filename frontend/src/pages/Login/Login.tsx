import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Login.css';

interface UserResponse {
  id: number;
  username: string;
  date_of_birth: string;
}

interface LoginProps {
  onLogin: () => void;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [dob, setDob] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post<UserResponse>(
        'http://localhost:8000/login',
        {
          username,
          date_of_birth: dob,
        },
        {
          headers: { 'Content-Type': 'application/json' },
        }
      );

      localStorage.setItem('user', JSON.stringify(response.data));
      localStorage.setItem('loginTime', Date.now().toString()); // Add this line

      onLogin();
      navigate('/welcome');
    } catch (err) {
      alert('Login failed');
      console.error(err);
    }
  };

  return (
    <div className="container">
      <h2>Login</h2>
      <form className="login-form" onSubmit={handleSubmit}>
        <div className="form-row">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-row">
          <label htmlFor="dob">Date of Birth</label>
          <input
            type="date"
            id="dob"
            value={dob}
            onChange={(e) => setDob(e.target.value)}
            required
          />
        </div>
        <div className="form-row">
          <button type="submit">Login</button>
        </div>
      </form>
    </div>
  );
};

export default Login;
