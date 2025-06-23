// src/pages/ChatPage.tsx
import { useState } from 'react';

type ChatPageProps = {
  userId: string;
  onClose: () => void;
};

const ChatPage = ({ userId, onClose }: ChatPageProps) => {
  const [messages, setMessages] = useState<{ sender: string; text: string }[]>([]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { sender: 'You', text: input }]);
      setInput('');
      // Here you would send the message to your backend or agent
    }
  };

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
        <div className="mb-4 text-gray-700">
          Chat window for user: <span className="font-semibold">{userId}</span>
        </div>
        <div className="border rounded p-4 bg-gray-50 text-gray-600 h-48 overflow-y-auto mb-4">
          {messages.length === 0 ? (
            <div>No messages yet.</div>
          ) : (
            messages.map((msg, idx) => (
              <div key={idx} className="mb-2">
                <span className="font-semibold">{msg.sender}: </span>
                <span>{msg.text}</span>
              </div>
            ))
          )}
        </div>
        <div className="flex gap-2">
          <input
            className="flex-1 border rounded px-2 py-1"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
            placeholder="Type your message..."
          />
          <button
            className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700"
            onClick={handleSend}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
