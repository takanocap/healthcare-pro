import {useState, useEffect, useRef, useCallback} from 'react';

interface WebSocketConfig{
    url: string;
    onMessage: (message: MessageEvent) => void; // can be any
    onOpen?: () => void;
    onClose?: () => void;
    onError?: (event: Event) => void;
    reconnectInterval?: number; // in milliseconds
    reconnectLimit?: number; // maximum number of reconnection attempts
}

export const useWebSocket = (config: WebSocketConfig) => {
    const {url, onMessage, onOpen, onClose, onError, reconnectInterval = 3000, reconnectLimit = 10} = config;
    const ws = useRef<WebSocket | null>(null);
    const [isConnected, setIsConnected] = useState(false);
    const reconnectAttempts = useRef(0);
    const reconnectTimeoutId = useRef<NodeJS.Timeout | null>(null);


    const connect = useCallback(() => {
        if(reconnectTimeoutId.current) {
            clearTimeout(reconnectTimeoutId.current);
        }
        if(ws.current && ws.current.readyState === WebSocket.OPEN) {
            return ;
        }
        ws.current = new WebSocket(url);

        ws.current.onopen = () => {
            setIsConnected(true);
            reconnectAttempts.current = 0;
            onOpen?.();
        };

        ws.current.onmessage = (event) => {
            try {
                const parsedMessages = JSON.parse(event.data);
                onMessage(parsedMessages);
            } catch (e) {
                console.error('Error parsing message:', e, event.data);
            }
        };

        ws.current.onclose = (event) => {
            setIsConnected(false);
            onClose?.();
            console.warn(`WebSocket closed. Code: ${event.code}, Reason: ${event.reason}`);
            if(!event.wasClean && reconnectAttempts.current < reconnectLimit) {
                reconnectAttempts.current++;
                console.log(`Attempting to reconnect... (${reconnectAttempts.current}/${reconnectLimit})...`);
                reconnectTimeoutId.current = setTimeout(connect, reconnectInterval);
            }else{
                console.error(`WebSocket closed cleanly or reconnect limit reached. No further attempts will be made.`);
            }
        };

        ws.current.onerror = (event) => {
            setIsConnected(false);
            onError?.(event);
            console.error('WebSocket error:', event);
        };
    }, [url, onMessage, onOpen, onClose, onError, reconnectInterval, reconnectLimit]);
    
    useEffect(() => {
        connect();
        return () => {
            if(reconnectTimeoutId.current) {
                clearTimeout(reconnectTimeoutId.current);
            }
            if(ws.current && ws.current.readyState === WebSocket.OPEN) {
                ws.current.close(1000, 'Component unmounted cleanly ');
               
            }
        };
    }, [connect]);

    const sendMessage = useCallback((message: any) => {
        if(ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify(message));
        } else {
            console.warn(`WebSocket is not open. Cannot send message: ${message}`);
        }
    }, []);

    return { isConnected, sendMessage};
}