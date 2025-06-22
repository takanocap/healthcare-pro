import React from 'react';

interface HeaderProps {
  username?: string;
  onLogout: () => void;
}

const Header: React.FC<HeaderProps> = ({ username, onLogout }) => {
  return (
    <header className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white p-4 shadow-lg rounded-b-lg">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-2xl font-bold">Clinical Insights</h1>
        {username && (
          <div className="flex items-center space-x-4">
            <span className="text-lg">Welcome, <span className="font-semibold">{username}</span>!</span>
            <button
              onClick={onLogout}
              className="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-full shadow-md transition duration-300 ease-in-out transform hover:scale-105"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;