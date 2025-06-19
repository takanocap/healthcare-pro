import React, { useState, useEffect, useContext } from 'react';
import MessageInput from '../components/MessageInput';
import { AuthContext } from '../contexts/AuthContext';
import { getMessages, createMessage, getInsights } from '../services/api';
import { connectWebSocket, disconnectWebSocket } from '../services/websocket';
import { Message } from '../types/api';
import { ClinicalInsight } from '../types/api';
import { Link } from 'react-router-dom';
import { getQuestionnaires } from '../services/api'; // Import for questionnaires

const HomePage: React.FC = () => {
  const { user, token } = useContext(AuthContext);
  const [messages, setMessages] = useState<Message[]>([]);
  const [insights, setInsights] = useState<ClinicalInsight[]>([]);
  const [activeQuestionnaires, setActiveQuestionnaires] = useState<any[]>([]); // Using 'any' for simplicity
  const [wsMessage, setWsMessage] = useState<string | null>(null);

  useEffect(() => {
    if (user && token) {
      // Fetch initial data
      fetchMessages();
      fetchInsights();
      fetchActiveQuestionnaires();

      // Connect WebSocket
      const ws = connectWebSocket(user.id.toString(), (event) => {
        const data = JSON.parse(event.data);
        console.log('WS Message received:', data);
        setWsMessage(JSON.stringify(data, null, 2)); // Display raw WS message for debugging

        // Handle different WebSocket message types
        if (data.type === 'agent_response') {
          // If it's an agent response, add it to messages
          setMessages((prevMessages) => [
            ...prevMessages,
            {
              id: Date.now(), // Dummy ID
              user_id: user.id,
              content: data.content,
              role: 'assistant',
              timestamp: new Date().toISOString(),
            },
          ]);
        } else if (data.type === 'new_insight') {
          // If it's a new insight, fetch insights again
          fetchInsights();
          alert(`New Insight: ${data.data.title}`); // Simple notification
        } else if (data.type === 'new_questionnaire') {
          fetchActiveQuestionnaires(); // Refresh active questionnaires
          alert(`New Questionnaire Available: ${data.data.title}`); // Simple notification
        }
      });

      return () => {
        disconnectWebSocket(ws);
      };
    }
  }, [user, token]);

  const fetchMessages = async () => {
    try {
      if (token) {
        const fetchedMessages = await getMessages(token);
        setMessages(fetchedMessages);
      }
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const fetchInsights = async () => {
    try {
      if (token) {
        const fetchedInsights = await getInsights(token);
        setInsights(fetchedInsights);
      }
    } catch (error) {
      console.error('Error fetching insights:', error);
    }
  };

  const fetchActiveQuestionnaires = async () => {
    try {
      if (token) {
        const fetchedQuestionnaires = await getQuestionnaires(token);
        setActiveQuestionnaires(fetchedQuestionnaires);
      }
    } catch (error) {
      console.error('Error fetching active questionnaires:', error);
    }
  };

  const handleSendMessage = async (content: string) => {
    try {
      if (token && user) {
        // Add user's message to display immediately
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            id: Date.now(), // Dummy ID for optimistic update
            user_id: user.id,
            content: content,
            role: 'user',
            timestamp: new Date().toISOString(),
          },
        ]);
        await createMessage(token, content);
        // Messages will be refetched by a WS event or can be done here.
        // For PoC, let agent respond via WS and we fetch all messages after.
        fetchMessages();
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="flex flex-col md:flex-row w-full h-full space-y-4 md:space-y-0 md:space-x-4">
      {/* Messages Section */}
      <div className="flex flex-col flex-1 bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold mb-4 text-gray-800 border-b pb-2">Messages</h2>
        <div className="flex-grow overflow-y-auto pr-2 custom-scrollbar space-y-4">
          {messages.length === 0 ? (
            <p className="text-gray-500">No messages yet. Start a conversation!</p>
          ) : (
            messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-md p-3 rounded-lg shadow-sm ${
                    msg.role === 'user'
                      ? 'bg-blue-500 text-white rounded-br-none'
                      : 'bg-gray-200 text-gray-800 rounded-bl-none'
                  }`}
                >
                  <p>{msg.content}</p>
                  <span className="text-xs opacity-75 mt-1 block">
                    {new Date(msg.timestamp).toLocaleString()}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
        <div className="mt-4">
          <MessageInput onSendMessage={handleSendMessage} />
        </div>
      </div>

      {/* Insights and Questionnaires Section */}
      <div className="flex flex-col w-full md:w-1/3 space-y-4">
        {/* Insights */}
        <div className="bg-white rounded-lg shadow-md p-6 flex-1 flex flex-col">
          <h2 className="text-2xl font-bold mb-4 text-gray-800 border-b pb-2">Clinical Insights</h2>
          <div className="flex-grow overflow-y-auto pr-2 custom-scrollbar space-y-3">
            {insights.length === 0 ? (
              <p className="text-gray-500">No insights yet. Check back later!</p>
            ) : (
              insights.map((insight) => (
                <div key={insight.id} className="border border-gray-200 p-4 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors duration-200">
                  <h3 className="font-semibold text-lg text-blue-700">{insight.title}</h3>
                  <p className="text-gray-700 text-sm mt-1">{insight.content}</p>
                  <p className="text-xs text-gray-500 mt-2">
                    Generated by: {insight.generated_by_agent || 'N/A'} | Severity: {insight.severity || 'N/A'}
                  </p>
                  <p className="text-xs text-gray-500">
                    {new Date(insight.created_at || '').toLocaleString()}
                  </p>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Active Questionnaires */}
        <div className="bg-white rounded-lg shadow-md p-6 flex-1 flex flex-col">
          <h2 className="text-2xl font-bold mb-4 text-gray-800 border-b pb-2">Active Questionnaires</h2>
          <div className="flex-grow overflow-y-auto pr-2 custom-scrollbar space-y-3">
            {activeQuestionnaires.length === 0 ? (
              <p className="text-gray-500">No active questionnaires.</p>
            ) : (
              activeQuestionnaires.map((q) => (
                <Link
                  key={q.id}
                  to={`/questionnaire/${q.id}`}
                  className="block border border-gray-200 p-4 rounded-lg bg-green-50 hover:bg-green-100 transition-colors duration-200 cursor-pointer"
                >
                  <h3 className="font-semibold text-lg text-green-700">{q.title}</h3>
                  <p className="text-gray-700 text-sm mt-1">{q.description || 'No description.'}</p>
                  <p className="text-xs text-gray-500 mt-2">Questions: {q.questions.length}</p>
                </Link>
              ))
            )}
          </div>
        </div>

        {/* WebSocket Raw Message Display (for debugging) */}
        {wsMessage && (
          <div className="bg-gray-800 text-white rounded-lg shadow-md p-4 mt-4">
            <h3 className="text-xl font-bold mb-2">Raw WS Message:</h3>
            <pre className="whitespace-pre-wrap text-sm">{wsMessage}</pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default HomePage;