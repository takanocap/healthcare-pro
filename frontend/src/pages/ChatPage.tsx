import React, { useState, useEffect, useRef } from "react";
import { useAuth } from "../context/AuthContext";
import ChatInterface from "../components/ChatInterface";
import SocketService from "../services/socket";
import { Socket } from "socket.io-client";

interface Question {
  id: number;
  question: string;
  options: string[];
}

interface Message {
  author: string;
  text: string;
}

const ChatPage = () => {
  const [questionnaire, setQuestionnaire] = useState<Question[] | null>(null);
  const { token, logout } = useAuth();
  const [socket, setSocket] = useState<Socket | null>(null);
  const [pendingInsight, setPendingInsight] = useState(false);
  const addBotMessageRef = useRef<(msg: Message) => void>(() => {});

  useEffect(() => {
    if (token) {
      const socketService = new SocketService(token);
      setSocket(socketService.getSocket());
    }
  }, [token]);

  const handleReceiveQuestionnaire = (questions: Question[]) => {
    setQuestionnaire(questions);
  };

  const handleQuestionnaireSubmit = async () => {
    setQuestionnaire(null);
    // After questionnaire is submitted, fetch insight and add as bot message
    // if (token && addBotMessageRef.current) {
    if (addBotMessageRef.current) {
      setPendingInsight(true);
      try {
        const response = await fetch("http://localhost:8000/questionnaires", {
        //   headers: {
        //     Authorization: `Bearer ${token}`,
        //   },
        });
        const data = await response.json();
        addBotMessageRef.current({
          author: "insight-agent",
          text: data.insight,
        });
      } catch (e) {
        addBotMessageRef.current({
          author: "insight-agent",
          text: "(Failed to load insight)",
        });
      } finally {
        setPendingInsight(false);
      }
    }
  };

  if (!socket) {
    return <div>Connecting to chat service...</div>;
  }

  return (
    <div style={{ padding: "20px", maxWidth: "800px", margin: "auto" }}>
      <button
        onClick={logout}
        style={{
          position: "absolute",
          top: "10px",
          right: "10px",
          padding: "8px 16px",
          borderRadius: "4px",
          border: "none",
          background: "#dc3545",
          color: "white",
          cursor: "pointer",
        }}
      >
        Logout
      </button>
      {!questionnaire && <h2>Welcome! How are you feeling today?</h2>}
      <ChatInterface
        onReceiveQuestionnaire={handleReceiveQuestionnaire}
        onQuestionnaireSubmit={handleQuestionnaireSubmit}
        questionnaire={questionnaire}
        socket={socket}
        setAddBotMessage={(fn) => {
          addBotMessageRef.current = fn;
        }}
        pendingInsight={pendingInsight}
      />
    </div>
  );
};

export default ChatPage;