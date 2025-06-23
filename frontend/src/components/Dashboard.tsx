
import React, {use, useEffect, useState} from "react";
// import AuthContext from "../contexts/AuthContext";
import { AuthContext } from "../contexts/AuthContext"
import {useWebSocket} from "../hooks/useWebSocket";
import MessageBubble from "./MessageBubble";


interface Message {
    id: string;
    content: string;
    sender: string;
    timestamp: string;
}

const Dashboard: React.FC = () => {
    const { userName, userId, token, logout } = React.useContext(AuthContext);
    const [messages, setMessages] = useState<Message[]>([]);
    const [newMessageText, setNewMessageText] = useState("");
    // const backendUrl = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";
    const backendUrl =  "http://localhost:8000";

    useEffect(() => {
        const fetchHistoricalMessages = async () => {
            if (!token || !userName) return;
            try {
                const response = await fetch(`${backendUrl}/api/v1/messages?user_name=${userName}`, {
                    headers: {'Authorization': `Bearer ${token}`}
                })
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data: Message[] = await response.json();
                setMessages(data.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()));
            } catch (error) {
                console.error("Error fetching historical messages:", error);
                
            }
        };
        fetchHistoricalMessages();
    }, [token, userName, backendUrl]);
    const {isConnected, sendMessage} = useWebSocket({
        url: `${backendUrl.replace('http', 'ws')}/ws/${userId}?token=${token}`,
        onMessage: (event: MessageEvent) => {
            try {
                const newMessage: Message = JSON.parse(event.data);
                setMessages(prevMessages => {
                    if (!prevMessages.some(msg => msg.id === newMessage.id)) {
                        return [...prevMessages, newMessage].sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());
                    }
                    return prevMessages;
                });
            } catch (err) {
                console.error("Failed to parse WebSocket message:", err);
            }
        },
        onOpen: () => console.log("Dashboard WebSocket connected"),
        onClose: () => console.log("Dashboard WebSocket disconnected"),
        onError: (e) => console.error("WebSocket error:", e),
    });

    const handleSendMessage = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newMessageText.trim() || !userId || !token) return;

        try {
            const response = await fetch(`${backendUrl}/api/v1/messages`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', 
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    userId,
                    input_type: "text_message",
                    content: newMessageText.trim(),
                    sender: userName,
                    timestamp: new Date().toISOString()
                })
            });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status} Failed to send message via REST `);
            setNewMessageText("");
            
        } catch (error) {
            console.error("Error sending message:", error);
            
        }
    };
    // if(!userName || !userId) {
    //     return (
    //         <p className="text-center text-gray-700">
    //             Please log in to view your dashboard.
    //         </p>
    //     );
    // }
    return (
        <div className="flex flex-col h-full bg-white round-lg shadow-lg overflow-hidden md: max-w-xl md:mx-auto">
            <header className="bg-blue-600 text-white p-4">
                <h1 className="text-2xl font-bold">Welcome, {userName}!</h1>
                <button
                    className="mt-2 bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded"
                    onClick={logout}
                >
                    Logout
                </button>
            </header>
            <div className="flex-1  p-4 overflow-y-auto space-y-3 bg-gray-50">
                {messages.length === 0 ? (
                    <p className="text-gray-500 text-center">No messages yet. Start the conversation!</p>
                ) : (
                    messages.map((msg) => (
                        <MessageBubble
                            key={msg.id}
                            message={msg}
                            // isCurrentUser={msg.sender === userName}
                        />
                    ))
                )}
            </div>

            <form className="p-4 bg-gray-100 flex space-x-2" onSubmit={handleSendMessage}>
                <input
                    type="text"
                    value={newMessageText}
                    onChange={(e) => setNewMessageText(e.target.value)}
                    placeholder={isConnected ? "Type your response..." : "connecting to chat..."}
                    className="flex-1 p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                    disabled={!isConnected}
                />
                <button
                    type="submit"
                    disabled={!isConnected || !newMessageText.trim()}
                    className={`px-4 py-2 text-white font-bold rounded ${isConnected ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-400 cursor-not-allowed'}`}
                >
                    Send
                </button>
            </form>
            <div className={`text-center txt-xs py-1 ${isConnected ? `bg-green-100 text-green-700` : 'bg-red-100 text-red-700'}`}>
                {isConnected ? "WebSocket is connected" : "WebSocket is disconnected Attempting to reconnect..."}
            </div>
        </div>

        
    );
}

export default Dashboard;