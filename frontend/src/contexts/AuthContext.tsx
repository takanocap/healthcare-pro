
import React, { createContext, useState, useEffect, ReactNode } from 'react';
import { loginUser, registerUser } from '../services/api';
// Update the import path below if your types are located elsewhere, e.g.:
import { UserPublic, Token } from '../types/api';
// If the file does not exist, create 'frontend/src/types/api.d.ts' with the following content:
// export interface UserPublic {
//   id: number;
//   username: string;
//   email: string;
//   is_active: boolean;
// }
// export interface Token {
//   access_token: string;
// }

interface AuthContextType {
  isAuthenticated: boolean;
  user: UserPublic | null;
  token: string | null;
   userName: string | null;
    userId: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string, email?: string) => Promise<void>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  user: null,
  userName: null,
  userId: null,
  token: null,
  login: async () => {},
  register: async () => {},
  logout: () => {},
});

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<UserPublic | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true); // To prevent flashing unauthenticated state

  useEffect(() => {
    // Attempt to load token and user from localStorage on mount
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');

    if (storedToken && storedUser) {
      try {
        const parsedUser: UserPublic = JSON.parse(storedUser);
        setToken(storedToken);
        setUser(parsedUser);
        setIsAuthenticated(true);
      } catch (e) {
        console.error('Failed to parse stored user or token:', e);
        logout(); // Clear invalid data
      }
    }
    setLoading(false);
  }, []);

  const login = async (username: string, password: string) => {
    try {
      const response: Token = await loginUser(username, password);
      const fetchedToken = response.access_token;
      // In a real app, you'd have an endpoint to get user details after login
      // For simplicity, let's assume we can derive basic user info or store it
      // For now, dummy user ID from a hypothetical response or regenerate
      const dummyUser: UserPublic = {
          id: Math.floor(Math.random() * 1000) + 1, // Placeholder ID
          username: username,
          email: `${username}@example.com`,
          is_active: true
      };

      setToken(fetchedToken);
      setUser(dummyUser);
      setIsAuthenticated(true);
      localStorage.setItem('token', fetchedToken);
      localStorage.setItem('user', JSON.stringify(dummyUser)); // Store user info
    } catch (error: any) {
      console.error('Login error:', error);
      throw new Error(error.response?.data?.detail || 'Login failed.');
    }
  };

  const register = async (username: string, password: string, email?: string) => {
    try {
      await registerUser(username, password, email);
      // No token generated directly after register in this PoC, user needs to login
    } catch (error: any) {
      console.error('Registration error:', error);
      throw new Error(error.response?.data?.detail || 'Registration failed.');
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  if (loading) {
    // Optionally render a loading spinner or splash screen
    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="text-xl text-gray-700">Loading application...</div>
        </div>
    );
  }

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        user,
        token,
        userName: user ? user.username : null,
        userId: user ? String(user.id) : null,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};