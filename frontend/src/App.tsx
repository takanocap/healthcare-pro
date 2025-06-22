
import PWABadge from './PWABadge.tsx'
import { AuthProvider } from './contexts/AuthContext';
import AppContent from './AppContent';

import './App.css'

function App() {
  
  return (
    <>
       <AuthProvider>
          <AppContent />
      </AuthProvider>
      <PWABadge />
    </>
  )
}

export default App
