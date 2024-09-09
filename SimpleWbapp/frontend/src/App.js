import React, { useEffect, useState } from 'react';

function App() {
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        const eventSource = new EventSource('http://localhost:8000/stream');

        eventSource.onmessage = function (event) {
            setMessages(prevMessages => [...prevMessages, event.data]);
        };

        eventSource.onerror = function (error) {
            console.error('EventSource failed:', error);
            eventSource.close();
        };

        return () => {
            eventSource.close();
        };
    }, []);

    return (
        <div>
            <h1>Streamed Messages</h1>
            <ul>
                {messages.map((message, index) => (
                    <li key={index}>{message}</li>
                ))}
            </ul>
        </div>
    );
}

export default App;