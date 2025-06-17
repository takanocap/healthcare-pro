import {useState} from 'react';
import './ChatUI.css'; // Assuming you have a CSS file for styling
// import { useTranslation } from 'react-i18next';
import axios from 'axios';


interface Message {
  user: 'patient' | 'agent';
  text: string;
}
export default function ChatUI() {
   const [messages, setMessages] = useState<Message[]>([]);
   const [input, setInput] = useState<string>('');

   const handleSend = async () => {
    const trimmedInput = input.trim();
    if (!trimmedInput) return;

    const updatedMessages: Message[] = [...messages, { user: 'patient', text: trimmedInput }];
    setMessages(updatedMessages);
    setInput('');

    try {
        const response = await axios.post<{reply: string}>('http://localhost:5000/api/v1/companion/respond', {
          message: trimmedInput,
          patientId: '12345-ABCD-67890-EFGH', // test value
        });
        setMessages([...updatedMessages, { user: 'agent', text: response.data.reply }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages([...updatedMessages, { user: 'agent', text: 'Error: Unable to get response from the server.' }]);
    }
   }


  return (
    <div className='chat-container'>
      <div className='chat-messages'>
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.user}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className='chat-input'>
        <input
          type='text'
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder='Type your message...'
          onKeyDown={e=> e.key === 'Enter' && handleSend()}
        />
        <button onClick={handleSend}>Send</button>
    </div>
    </div>
  );
}

