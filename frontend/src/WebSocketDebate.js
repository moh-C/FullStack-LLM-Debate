import React, { useState, useEffect, useRef } from 'react';

const WebSocketDebate = () => {
    const [messages, setMessages] = useState([]);
    const [error, setError] = useState(null);
    const [isConnected, setIsConnected] = useState(false);
    const ws = useRef(null);

    useEffect(() => {
        // Connect to WebSocket
        ws.current = new WebSocket('ws://localhost:8000/ws');

        ws.current.onopen = () => {
            console.log('WebSocket connected');
            setIsConnected(true);
            // Request first result
            ws.current.send('start');
        };

        ws.current.onmessage = (event) => {
            if (event.data === '<END_TOKEN_WEBSOCKET>') {
                // End of current message, request next
                ws.current.send('continue');
            } else {
                setMessages(prev => [...prev, event.data]);
            }
        };

        ws.current.onerror = (error) => {
            console.error('WebSocket error:', error);
            setError('WebSocket error occurred');
        };

        ws.current.onclose = () => {
            console.log('WebSocket disconnected');
            setIsConnected(false);
        };

        // Clean up on unmount
        return () => {
            if (ws.current) {
                ws.current.close();
            }
        };
    }, []);

    return (
        <div>
            <h2>Debate Progress</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {isConnected ? (
                <p style={{ color: 'green' }}>Connected to WebSocket</p>
            ) : (
                <p style={{ color: 'red' }}>Disconnected from WebSocket</p>
            )}
            <div style={{
                border: '1px solid #ccc',
                padding: '10px',
                maxHeight: '400px',
                overflowY: 'auto'
            }}>
                {messages.map((msg, index) => (
                    <p key={index}>{msg}</p>
                ))}
            </div>
        </div>
    );
};

export default WebSocketDebate;