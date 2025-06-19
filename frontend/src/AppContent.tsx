import { useEffect, useContext } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import HomePage from './pages/HomePage';
import QuestionnairePage from './pages/QuestionnairePage';
import Header from './components/Header';
import { AuthContext } from './contexts/AuthContext';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';


function AppContent() {
  const { isAuthenticated, user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    } else if (window.location.pathname === '/login' || window.location.pathname === '/register') {
      
      navigate('/');
    }
  }, [isAuthenticated, navigate]);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col font-inter">
      {isAuthenticated && <Header username={user?.username} onLogout={logout} />}
      <main className="flex-grow container mx-auto p-4 flex">
        <Routes>
          <Route path="/" element={isAuthenticated ? <HomePage /> : <LoginPage />} />
          <Route path="questionnaire/:id" element={isAuthenticated ? <QuestionnairePage /> : <LoginPage />} />
          <Route path="login" element={<LoginPage />} />
          <Route path="register" element={<RegisterPage />} />
        </Routes>
      </main>
      <footer className="bg-gray-800 text-white text-center p-4">
        <p>&copy; {new Date().getFullYear()} Healthcare PRO </p>
      </footer>
    </div>
  );
}

export default AppContent;