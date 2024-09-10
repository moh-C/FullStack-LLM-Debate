import React, { useState } from 'react';
import { testEndpoint } from '../utils/api';

const ApiTestDashboard = () => {
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleTestEndpoint = async (endpoint) => {
        setIsLoading(true);
        const response = await testEndpoint(endpoint);
        setMessage(JSON.stringify(response, null, 2));
        setIsLoading(false);
    };

    return (
        <div>
            <button onClick={() => handleTestEndpoint('/')} disabled={isLoading}>Test Root</button>
            <button onClick={() => handleTestEndpoint('/health')} disabled={isLoading} style={{ marginLeft: '10px' }}>Test Health</button>
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

export default ApiTestDashboard;