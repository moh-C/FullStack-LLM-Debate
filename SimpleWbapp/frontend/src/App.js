import React, { useState, useEffect, useCallback, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css';

function App() {
    const [input, setInput] = useState('');
    const [output, setOutput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isConnected, setIsConnected] = useState(false);
    const retryCountRef = useRef(0);
    const socketRef = useRef(null);

    const connectWebSocket = () => {
        const ws = new WebSocket('ws://localhost:8000/ws');

        ws.onopen = () => {
            setIsConnected(true);
            retryCountRef.current = 0;
            console.log('WebSocket Connected');
        };

        ws.onmessage = (event) => {
            if (event.data === '[DONE]') {
                setIsLoading(false);
            } else {
                setOutput(prevOutput => prevOutput + event.data);
            }
        };

        ws.onerror = (error) => {
            console.error('WebSocket Error:', error);
            setIsLoading(false);
        };

        ws.onclose = () => {
            setIsConnected(false);
            console.log('WebSocket Disconnected');
            if (retryCountRef.current < 3) {  // Try to reconnect up to 3 times
                setTimeout(() => {
                    retryCountRef.current += 1;
                    connectWebSocket();
                }, 1000);
            }
        };

        socketRef.current = ws;
    };

    useEffect(() => {
        connectWebSocket();
        return () => {
            if (socketRef.current) {
                socketRef.current.close();
            }
        };
    }, []); // Empty dependency array ensures this runs once, similar to componentDidMount

    const handleGenerate = useCallback(() => {
        const socket = socketRef.current;
        if (!socket || socket.readyState !== WebSocket.OPEN) {
            console.error('WebSocket is not connected');
            return;
        }
        setIsLoading(true);
        setOutput('');
        socket.send(JSON.stringify({ prompt: input }));
    }, [input]);

    return (
        <div className="container">
            <h1>AI Assistant</h1>
            <div className="input-container">
                <label htmlFor="prompt">Your Prompt</label>
                <textarea
                    id="prompt"
                    rows="4"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Enter your prompt here..."
                />
            </div>
            <button onClick={handleGenerate} disabled={isLoading || !isConnected}>
                {isLoading ? 'Generating...' : 'Generate'}
            </button>
            <div className="output-container">
                <h2>Output:</h2>
                <ReactMarkdown>{output || 'Your response will appear here...'}</ReactMarkdown>
            </div>
        </div>
    );
}

export default App;