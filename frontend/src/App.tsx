// App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login/Login';
import Welcome from './pages/Welcome/Welcome';
import ProtectedRoute from './routes/ProtectedRoute';
import { isAuthenticated } from './utils/auth';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        {/* Redirect root based on auth status */}
        <Route
          path="/"
          element={
            isAuthenticated() ? (
              <Navigate to="/welcome" replace />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />

        <Route
          path="/login"
          element={
            isAuthenticated() ? (
              <Navigate to="/welcome" replace />
            ) : (
              <Login
                onLogin={() => {
                  /* Handle login success if needed */
                }}
              />
            )
          }
        />

        <Route
          path="/welcome"
          element={
            <ProtectedRoute>
              <Welcome />
            </ProtectedRoute>
          }
        />

        {/* Catch-all route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
};

export default App;
