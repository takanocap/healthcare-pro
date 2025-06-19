import React from 'react'

interface MessageBubbleProps {
    message: {
        id: string;
        content: string;
        sender: string;
        timestamp: string;
    };
}


const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
    const isAgent = message.sender !== 'usersSenderName';
  return (
    <div className={`flex items-start mb-4 ${isAgent ? 'justify-start' : 'justify-end'}`}>
      <div className={`max-w-xs p-3 rounded-lg ${isAgent ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'} shadow-md`}>
        <p className="text-sm font-semibold">{message.sender}</p>
        <p className="text-sm">{message.content}</p>
        <span className="text-xs text-gray-500 mt-1">{new Date(message.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit' })}</span>
    </div>
    </div>
  );
};

export default MessageBubble;