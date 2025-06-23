
import React, { useState, useEffect } from "react";
import { Socket } from "socket.io-client";
import { useAuth } from "../context/AuthContext";
import Questionnaire from "./Questionnaire";

interface Message {
  author: string;
  text: string;
}

interface Question {
  id: number;
  question: string;
  options: string[];
}

interface ChatInterfaceProps {
  onReceiveQuestionnaire: (questions: Question[]) => void;
  onQuestionnaireSubmit: () => void;
  questionnaire: Question[] | null;
  socket: Socket;
  setAddBotMessage?: (fn: (msg: Message) => void) => void;
  pendingInsight?: boolean;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  onReceiveQuestionnaire,
  onQuestionnaireSubmit,
  questionnaire,
  socket,
  setAddBotMessage,
  pendingInsight,
}) => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const { token } = useAuth();

  useEffect(() => {
    const handleConnect = () => console.log("Connected to socket server");
    const handleDisconnect = () =>
      console.log("Disconnected from socket server");
    const handleMessage = (data: Message) => {
      setMessages((prevMessages) => [...prevMessages, data]);
    };

    socket.on("connect", handleConnect);
    socket.on("disconnect", handleDisconnect);
    socket.on("message", handleMessage);

    return () => {
      socket.off("connect", handleConnect);
      socket.off("disconnect", handleDisconnect);
      socket.off("message", handleMessage);
    };
  }, [socket]);

  // Provide a function to add a bot message to the chat
  useEffect(() => {
    if (setAddBotMessage) {
      setAddBotMessage((msg: Message) => {
        setMessages((prev) => [...prev, msg]);
      });
    }
  }, [setAddBotMessage]);

  const handleSendMessage = async () => {
    if (message.trim()) {
      const userMessage: Message = { author: "user", text: message };
      setMessages([...messages, userMessage]);
      socket.emit("message", message);

      if (messages.length === 0) {
        // First message, post to /answer
        try {
          const response = await fetch("http://localhost:8000/answer", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ answer: message }),
          });

          if (!response.ok) {
            throw new Error("Failed to fetch questionnaire");
          }

          const data = await response.json();
          onReceiveQuestionnaire(data.questionnaire);
        } catch (error) {
          console.error("Error fetching questionnaire:", error);
        }
      }

      setMessage("");
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "80vh",
        border: "1px solid #ccc",
        borderRadius: "8px",
        padding: "16px",
        marginTop: "20px",
      }}
    >
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          marginBottom: "16px",
          borderBottom: "1px solid #eee",
        }}
      >
        {messages.map((msg, index) =>
          msg ? (
            <div
              key={index}
              style={{
                marginBottom: "8px",
                padding: "8px",
                background:
                  msg.author === "user"
                    ? "#d1e7dd"
                    : msg.author === "insight-agent"
                    ? "#e2e3e5"
                    : "#f8d7da",
                borderRadius: "4px",
                alignSelf: msg.author === "user" ? "flex-end" : "flex-start",
              }}
            >
              <strong>{msg.author}: </strong>
              {msg.text}
            </div>
          ) : null
        )}
        {questionnaire && (
          <div style={{ marginTop: "16px" }}>
            <Questionnaire
              questions={questionnaire}
              onSubmit={onQuestionnaireSubmit}
            />
          </div>
        )}
        {pendingInsight && (
          <div style={{ marginTop: "16px", color: "#888" }}>
            <em>Loading insight...</em>
          </div>
        )}
      </div>
      {!questionnaire && (
        <div style={{ display: "flex" }}>
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
            style={{
              flex: 1,
              padding: "8px",
              borderRadius: "4px",
              border: "1px solid #ccc",
            }}
          />
          <button
            onClick={handleSendMessage}
            style={{
              marginLeft: "8px",
              padding: "8px 16px",
              borderRadius: "4px",
              border: "none",
              background: "#007bff",
              color: "white",
              cursor: "pointer",
            }}
          >
            Send
          </button>
        </div>
      )}
    </div>
  );
};

export default ChatInterface;