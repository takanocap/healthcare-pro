// import React from "react";
// import {
//   BrowserRouter as Router,
//   Route,
//   Routes,
//   Navigate,
// } from "react-router-dom";
// import LoginPage from "./pages/LoginPage";
// import ChatPage from "./pages/ChatPage";
// import { AuthProvider, useAuth } from "./context/AuthContext";

// const AppRoutes = () => {
//   const { isAuthenticated } = useAuth();

//   return (
//     <Routes>
//       {/* <Route
//         path="/"
//         element={!isAuthenticated ? <LoginPage /> : <Navigate to="/chat" />}
//       /> */}
//       <Route
//         path="/chat"
//         element={!isAuthenticated ? <ChatPage /> : <Navigate to="/" />}
//       />
//     </Routes>
//   );
// };

// function App() {
//   return (
    
//       <AuthProvider>
//         <AppRoutes />
//       </AuthProvider>
    
//   );
// }

// export default App;

import { useState, useEffect } from 'react';
import PWABadge from './PWABadge.tsx'
// import { AuthProvider } from './contexts/AuthContext';
// import AppContent from './AppContent';
import axios from 'axios';

import './App.css'

// Assume BASE_URL is your FastAPI backend URL (e.g., http://localhost:8000)
const BASE_URL = 'http://localhost:8000';
const VAPID_PUBLIC_KEY = 'YOUR_VAPID_PUBLIC_KEY_FROM_BACKEND'; // Get this from your backend setup

// Dummy ChatWindow component for demonstration
function ChatWindow({ userId, onClose }: { userId: string, onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg p-6 max-w-md w-full relative">
        <button
          className="absolute top-2 right-2 text-gray-500 hover:text-gray-800"
          onClick={onClose}
        >
          ×
        </button>
        <h2 className="text-xl font-bold mb-4">Chat with Companion Agent</h2>
        <div className="mb-4 text-gray-700">Chat window for user: <span className="font-semibold">{userId}</span></div>
        {/* Replace this with your actual chat UI */}
        <div className="border rounded p-4 bg-gray-50 text-gray-600">Chat functionality goes here.</div>
      </div>
    </div>
  );
}

function App() {
  const [userId, setUserId] = useState(''); // User ID obtained after login/registration
  const [notificationPermission, setNotificationPermission] = useState(Notification.permission);
  const [message, setMessage] = useState('');
  const [showChat, setShowChat] = useState(false);

  // --- Service Worker Registration and Push Subscription Logic ---
  useEffect(() => {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/service-worker.js')
        .then(registration => {
          console.log('Service Worker registered with scope:', registration.scope);
        })
        .catch(error => {
          console.error('Service Worker registration failed:', error);
        });
    }

    if (Notification.permission !== 'granted' && Notification.permission !== 'denied') {
      Notification.requestPermission().then(permission => {
        setNotificationPermission(permission);
        if (permission === 'granted' && 'serviceWorker' in navigator) {
          navigator.serviceWorker.ready.then(registration => {
            subscribeUserToPush(registration);
          });
        }
      });
    } else if (Notification.permission === 'granted' && 'serviceWorker' in navigator) {
      navigator.serviceWorker.ready.then(registration => {
        subscribeUserToPush(registration);
      });
      setNotificationPermission(Notification.permission);
    } else {
      setNotificationPermission(Notification.permission);
    }
  }, []); // Run once on mount

  // Function to subscribe user to push notifications
  const subscribeUserToPush = async (registration: ServiceWorkerRegistration) => {
    try {
      const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY),
      });

      console.log('Push Subscription:', subscription.toJSON());

      if (userId) {
        await axios.post(`${BASE_URL}/notifications/subscribe`, {
          userId: userId,
          subscription: subscription.toJSON(),
        });
        setMessage('Successfully subscribed to push notifications!');
      } else {
        setMessage('Please log in to subscribe to notifications.');
      }

    } catch (error) {
      console.error('Failed to subscribe the user:', error);
      setMessage('Failed to subscribe to push notifications. Please try again.');
    }
  };

  // Utility function for VAPID key conversion
  const urlBase64ToUint8Array = (base64String: string) => {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
      .replace(/\-/g, '+')
      .replace(/_/g, '/');
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  };

  // --- Trigger Companion Agent Check Logic ---
  const handleStartCompanionCheck = async () => {
    if (!userId) {
      setMessage('Please log in to trigger a companion check.');
      return;
    }
    setMessage('Requesting companion agent check...');
    try {
      const response = await axios.post(`${BASE_URL}/companion-agent/trigger-check`, {
        user_id: userId,
        trigger_source: "pwa_manual_check",
      });
      setMessage(`Companion agent check initiated successfully! Response: ${response.data.message}`);
      // Redirect to ChatPage using react-router-dom
      window.location.assign('/chat');
      console.log('Companion agent check response:', response.data);
    } catch (error) {
      console.error('Failed to trigger companion agent check:', error);
      setMessage('Failed to trigger companion agent check. Please try again.');
    }
  };

  // --- Simulated Login/User ID Setter (for demo purposes) ---
  const handleLogin = () => {
    setUserId('user-mock-123');
    setMessage('Logged in as user-mock-123. You can now subscribe to notifications and trigger checks.');
  };

  return (
    <>
      <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4 font-sans">
      <div className="bg-white p-8 rounded-lg shadow-md max-w-md w-full">
        <h1 className="text-2xl font-bold mb-6 text-center text-gray-800">Healthcare PRO</h1>

        {!userId ? (
        <button
          onClick={handleLogin}
          className="w-full  bg-blue-100 border border-blue-200 text-white-800 py-2 px-4 rounded-md hover:bg-blue-700 transition duration-300 mb-4"
        >
          Simulate Login (Set User ID)
        </button>
        ) : (
        <p className="text-center text-gray-700 mb-4">Logged in as: <span className="font-semibold">{userId}</span></p>
        )}

        {notificationPermission === 'default' && (
        <p className="text-center text-orange-500 mb-4">
          Please allow notification permissions in your browser.
        </p>
        )}
        {notificationPermission === 'denied' && (
        <p className="text-center text-red-500 mb-4">
          Notification permissions denied. Please enable them in your browser settings.
        </p>
        )}
        {notificationPermission === 'granted' && (
        <p className="text-center text-green-600 mb-4">
          Notifications are enabled!
        </p>
        )}

        <button
        onClick={handleStartCompanionCheck}
        className="w-full btn-green border border-blue-200 text-blue-800 py-3 px-4 rounded-md hover:bg-green-600 transition duration-300 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-75"
        disabled={!userId}
        >
        Start Companion Agent Check
        </button>

        {message && (
        <div className="mt-6 p-3 bg-blue-100 border border-blue-200 text-blue-800 rounded-md">
          {message}
        </div>
        )}
      </div>
      </div>
      <PWABadge />
      {/* Routing to ChatPage
      {showChat && userId && (
      <ChatPage userId={userId} onClose={() => setShowChat(false)} />
      )} */}
    </>
  );
}

export default App;
