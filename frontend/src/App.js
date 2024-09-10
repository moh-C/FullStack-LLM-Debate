import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

const App = () => {
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const testEndpoint = async (endpoint, method = 'get', data = null) => {
        setIsLoading(true);
        setMessage('');
        try {
            let response;
            if (method === 'get') {
                response = await axios.get(`${API_URL}${endpoint}`);
            } else if (method === 'post') {
                response = await axios.post(`${API_URL}${endpoint}`, data);
            }
            console.log(`${endpoint} response:`, response);
            setMessage(JSON.stringify(response.data, null, 2));
        } catch (error) {
            console.error(`Error from ${endpoint}:`, error.response || error);
            setMessage(`Error: ${error.response?.data?.detail || error.message}`);
        } finally {
            setIsLoading(false);
        }
    };

    const startDebate = () => {
        const debateData = {
            topic: "AI Ethics",
            name1: "Proponent",
            name2: "Opponent",
            questions: ["What are the main ethical concerns in AI development?"]
        };
        testEndpoint('/start_debate', 'post', debateData);
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
            <h1>API Test Dashboard</h1>
            <div style={{ marginBottom: '20px' }}>
                <button onClick={() => testEndpoint('/')} disabled={isLoading}>Test Root</button>
                <button onClick={() => testEndpoint('/health')} disabled={isLoading} style={{ marginLeft: '10px' }}>Test Health</button>
                <button onClick={startDebate} disabled={isLoading} style={{ marginLeft: '10px' }}>Start Debate</button>
            </div>
            {isLoading ? (
                <p>Loading...</p>
            ) : (
                <pre style={{
                    backgroundColor: '#f0f0f0',
                    padding: '10px',
                    borderRadius: '5px',
                    whiteSpace: 'pre-wrap',
                    wordWrap: 'break-word'
                }}>
                    {message || 'No message yet. Click a button to test an endpoint.'}
                </pre>
            )}
        </div>
    );
};

export default App;