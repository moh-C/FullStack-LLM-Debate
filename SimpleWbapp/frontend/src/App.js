import React, { useState, useEffect, useCallback } from 'react';

function App() {
    const [input, setInput] = useState('');
    const [output, setOutput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [socket, setSocket] = useState(null);

    useEffect(() => {
        const ws = new WebSocket('ws://localhost:8000/ws');
        setSocket(ws);

        ws.onopen = () => {
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
            console.log('WebSocket Disconnected');
        };

        return () => {
            ws.close();
        };
    }, []);

    const handleGenerate = useCallback(() => {
        if (socket && socket.readyState === WebSocket.OPEN) {
            setIsLoading(true);
            setOutput('');
            socket.send(JSON.stringify({ prompt: input }));
        } else {
            console.error('WebSocket is not connected');
        }
    }, [socket, input]);

    return (
        <div className="container">
            <h1>AI Assistant</h1>
            <div>
                <label htmlFor="prompt">Your Prompt</label>
                <textarea
                    id="prompt"
                    rows="4"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Enter your prompt here..."
                />
            </div>
            <button onClick={handleGenerate} disabled={isLoading || !socket || socket.readyState !== WebSocket.OPEN}>
                {isLoading ? 'Generating...' : 'Generate'}
            </button>
            <div>
                <h2>Output:</h2>
                <pre>{output || 'Your response will appear here...'}</pre>
            </div>
        </div>
    );
}

export default App;