// components/TopNavBar.tsx
import React from 'react';
import { AppBar, Toolbar, Typography, Box, Button } from '@mui/material';
import { LogoutOutlined } from '@mui/icons-material';
import { useLocation } from 'react-router-dom';
import logo from '../../assets/logo.png';


interface TopNavBarProps {
  onLogout?: () => void;
}

const TopNavBar: React.FC<TopNavBarProps> = ({ onLogout }) => {
  const location = useLocation();
  const isWelcomePage = location.pathname === '/welcome'; // Adjust if your welcome route is different

  return (
    <AppBar position="static" elevation={1} color="primary">
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <img src={logo} alt="Logo" style={{ height: 35, marginRight: 12 }} />
          <Typography variant="h6" component="div" sx={{ fontWeight: 'bold' }}>
            Healthcare PRO
          </Typography>
        </Box>

        {isWelcomePage && (
          <Button
            color="inherit"
            startIcon={<LogoutOutlined />}
            onClick={onLogout}
            sx={{ textTransform: 'none' }}
          >
            Logout
          </Button>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default TopNavBar;
