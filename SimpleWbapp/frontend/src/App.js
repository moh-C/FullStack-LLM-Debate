import React, { useState, useEffect, useCallback, useRef } from 'react';
import ReactMarkdown from 'react-markdown';

function App() {
    const [input, setInput] = useState('');
    const [output1, setOutput1] = useState('');
    const [output2, setOutput2] = useState('');
    const [isLoading1, setIsLoading1] = useState(false);
    const [isLoading2, setIsLoading2] = useState(false);
    const [isConnected1, setIsConnected1] = useState(false);
    const [isConnected2, setIsConnected2] = useState(false);
    const retryCountRef1 = useRef(0);
    const retryCountRef2 = useRef(0);
    const socketRef1 = useRef(null);
    const socketRef2 = useRef(null);

    const connectWebSocket = (socketRef, setIsConnected, retryCountRef, connectFunction) => {
        const ws = new WebSocket(connectFunction);

        ws.onopen = () => {
            setIsConnected(true);
            retryCountRef.current = 0;
            console.log('WebSocket Connected');
        };

        ws.onmessage = (event) => {
            if (event.data === '[DONE]') {
                if (socketRef === socketRef1) {
                    setIsLoading1(false);
                } else {
                    setIsLoading2(false);
                }
            } else {
                if (socketRef === socketRef1) {
                    setOutput1(prevOutput => prevOutput + event.data);
                } else {
                    setOutput2(prevOutput => prevOutput + event.data);
                }
            }
        };

        ws.onerror = (error) => {
            console.error('WebSocket Error:', error);
            if (socketRef === socketRef1) {
                setIsLoading1(false);
            } else {
                setIsLoading2(false);
            }
        };

        ws.onclose = () => {
            setIsConnected(false);
            console.log('WebSocket Disconnected');
            if (retryCountRef.current < 3) {  // Try to reconnect up to 3 times
                setTimeout(() => {
                    retryCountRef.current += 1;
                    connectWebSocket(socketRef, setIsConnected, retryCountRef, connectFunction);
                }, 1000);
            }
        };

        socketRef.current = ws;
    };

    useEffect(() => {
        connectWebSocket(socketRef1, setIsConnected1, retryCountRef1, 'ws://localhost:8000/ws1');
        connectWebSocket(socketRef2, setIsConnected2, retryCountRef2, 'ws://localhost:8000/ws2');

        return () => {
            if (socketRef1.current) {
                socketRef1.current.close();
            }
            if (socketRef2.current) {
                socketRef2.current.close();
            }
        };
    }, []); // Empty dependency array ensures this runs once, similar to componentDidMount

    const handleGenerate = useCallback(() => {
        const socket1 = socketRef1.current;
        const socket2 = socketRef2.current;
        if (!socket1 || socket1.readyState !== WebSocket.OPEN || !socket2 || socket2.readyState !== WebSocket.OPEN) {
            console.error('WebSocket is not connected');
            return;
        }
        setIsLoading1(true);
        setIsLoading2(true);
        setOutput1('');
        setOutput2('');
        socket1.send(JSON.stringify({ prompt: input }));
        socket2.send(JSON.stringify({ prompt: input }));
    }, [input]);

    return (
        <div className="app-container">
            <header className="app-header">
                <h1 className="app-title">AI Assistant</h1>
            </header>
            <main className="app-main">
                <div className="input-section">
                    <textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Enter your prompt here..."
                        className="input-textarea"
                    />
                    <button
                        onClick={handleGenerate}
                        disabled={isLoading1 || isLoading2 || !isConnected1 || !isConnected2}
                        className="generate-button"
                    >
                        {(isLoading1 || isLoading2) ? 'Generating...' : 'Generate'}
                    </button>
                </div>
                <div className="output-section">
                    <div className="output-card">
                        <h2 className="output-title">Output from LLM 1</h2>
                        <div className="output-content">
                            <ReactMarkdown>{output1 || 'Your response will appear here...'}</ReactMarkdown>
                        </div>
                    </div>
                    <div className="output-card">
                        <h2 className="output-title">Output from LLM 2</h2>
                        <div className="output-content">
                            <ReactMarkdown>{output2 || 'Your response will appear here...'}</ReactMarkdown>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}

export default App;