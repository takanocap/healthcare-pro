// components/WelcomePage.tsx
import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  CircularProgress,
  Alert,
  Paper,
  Divider,
  Container,
  AppBar,
  Toolbar
} from "@mui/material";
import { LogoutOutlined } from '@mui/icons-material';
import { AgentResponse, agentService, PatientData, PatientInteractionRequest } from '../../services/agentService';
import { useNavigate } from 'react-router-dom';
import './WelcomePage.css';
import TopNavBar from '../TopNavBar/TopNavBar';

// interface WelcomePageProps {
//   user: {
//     id: string;
//     name: string;
//     condition: string;
//     language: string;
//   };
// }

export const WelcomePage: React.FC = () => {
  const [agentResponse, setAgentResponse] = useState<AgentResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [userMessage, setUserMessage] = useState('');
  const [conversationHistory, setConversationHistory] = useState<Array<{
    sender: 'user' | 'agent';
    message: string;
    timestamp: Date;
  }>>([]);
    
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  console.log("User: ", user);
  
  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('loginTime');
    navigate('/login');
  };

  const patientData: PatientData = {
    id: user.id.toString(),
    name: user.username,
    condition: user.condition,
    language: user.language,
    last_checkin: localStorage.getItem(`last_checkin_${user.id}`) || undefined,
  };

  // Initiate check-in when component mounts
  useEffect(() => {
    initiateCheckin();
  }, []);

  const initiateCheckin = async () => {
    setLoading(true);
    setError(null);

    try {
      const requestBody: PatientInteractionRequest = {
        patient_id: user.id.toString(),
        interaction_type: "checkin",
        patient_data: patientData,
        // user_message: optional, include if needed
      };

      const response = await agentService.interactWithAgent(requestBody);

      setAgentResponse(response);
      setConversationHistory([
        {
          sender: "agent",
          message: response.agent_response.message,
          timestamp: new Date(),
        },
      ]);

      localStorage.setItem(`last_checkin_${user.id}`, new Date().toISOString());
    } catch (err) {
      setError("Failed to connect with your healthcare companion. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!userMessage.trim()) return;

    setLoading(true);
    const newMessage = userMessage;
    setUserMessage('');

    // Add user message to history
    setConversationHistory(prev => [...prev, {
      sender: 'user',
      message: newMessage,
      timestamp: new Date()
    }]);

    try {
      const requestBody: PatientInteractionRequest = {
        patient_id: user.id.toString(),
        interaction_type: "questionnaire",
        patient_data: patientData,
        user_message: newMessage,
      };

      const response = await agentService.interactWithAgent(requestBody);
      setConversationHistory(prev => [...prev, {
        sender: 'agent',
        message: response.agent_response.message,
        timestamp: new Date()
      }]);

      console.log("agent : ", response.agent_response.message);

      setAgentResponse(response);

    } catch (err) {
      setError('Failed to send message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
    <Box sx={{ flexGrow: 1, minHeight: '100px' }}>
      <TopNavBar onLogout={handleLogout} />      
      <Container maxWidth="md">
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            textAlign: 'center',
          }}
        >
          <Typography
            variant="h3"
            component="h1"
            sx={{
              fontWeight: 'bold',
              color: 'primary.main',
              mb: 2,
              mt: 2,
            }}
          >
            Welcome, {user.username}! 👋
          </Typography>
        </Box>
      </Container>      
    </Box>
    <Box sx={{ maxWidth: '95vw', mx: 'auto', p: 3 }}>
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Your Healthcare Companion
          </Typography>
          
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Paper 
            elevation={1} 
            sx={{ 
              p: 2, 
              mb: 2, 
              maxHeight: 400, 
              overflowY: 'auto',
              backgroundColor: '#f8f9fa'
            }}
          >
            {conversationHistory.map((item, index) => (
              <Box key={index} sx={{ mb: 2 }}>
                <Typography 
                  variant="body2" 
                  color={item.sender === 'agent' ? 'primary' : 'text.secondary'}
                  sx={{ fontWeight: 'bold', mb: 0.5 }}
                >
                  {item.sender === 'agent' ? '🤖 Healthcare Companion' : '👤 You'}
                </Typography>
                <Typography variant="body1" sx={{ 
                  p: 1.5, 
                  backgroundColor: item.sender === 'agent' ? '#e3f2fd' : '#fff',
                  borderRadius: 2,
                  border: '1px solid #e0e0e0'
                }}>
                  {item.message}
                </Typography>
              </Box>
            ))}
            
            {loading && (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <CircularProgress size={16} />
                <Typography variant="body2" color="text.secondary">
                  Companion is thinking...
                </Typography>
              </Box>
            )}
          </Paper>

          <Box sx={{ display: 'flex', gap: 2 }}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Type your response..."
              value={userMessage}
              onChange={(e) => setUserMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              disabled={loading}
            />
            <Button 
              variant="contained" 
              onClick={sendMessage}
              disabled={loading || !userMessage.trim()}
            >
              Send
            </Button>
          </Box>

          <Divider sx={{ my: 2 }} />

          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button 
              variant="outlined" 
              onClick={initiateCheckin}
              disabled={loading}
            >
              Start New Check-in
            </Button>
            <Button 
              variant="outlined" 
              onClick={() => {
                // Navigate to detailed questionnaire
                console.log('Navigate to detailed questionnaire');
              }}
              disabled={loading}
            >
              Complete Full Assessment
            </Button>
          </Box>
        </CardContent>
      </Card>

      {/* {agentResponse?.next_action && (
        <Alert severity="info">
          Next step: {agentResponse.next_action}
        </Alert>
      )} */}
    </Box>
    </>
  );
};
