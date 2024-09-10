import React, { useState, useEffect, useRef } from 'react';
import { startDebate, oneTurnDebate, getPersonas } from '../utils/api';

const DebateController = ({ debateStarted, setDebateStarted, setDebateResponses, setPersonas }) => {
    const [isLoading, setIsLoading] = useState(false);
    const [useWebSocket, setUseWebSocket] = useState(true);
    const ws = useRef(null);

    useEffect(() => {
        if (debateStarted && useWebSocket) {
            ws.current = new WebSocket('ws://localhost:8000/ws');
            ws.current.onmessage = (event) => {
                if (event.data === "<END_WEBSOCKET_TOKEN>") {
                    setIsLoading(false);
                } else {
                    const data = JSON.parse(event.data);
                    setDebateResponses(prev => [...prev, data]);
                }
            };
            return () => {
                if (ws.current) {
                    ws.current.close();
                }
            };
        }
    }, [debateStarted, useWebSocket, setDebateResponses]);

    const handleStartDebate = async () => {
        setIsLoading(true);
        const success = await startDebate();
        if (success) {
            setDebateStarted(true);
        }
        setIsLoading(false);
    };

    const handleOneTurnDebate = async () => {
        setIsLoading(true);
        if (useWebSocket && ws.current) {
            ws.current.send('next');
        } else {
            const response = await oneTurnDebate();
            if (response) {
                setDebateResponses(prev => [...prev, response]);
            }
            setIsLoading(false);
        }
    };

    const handleGetPersonas = async () => {
        setIsLoading(true);
        const personasData = await getPersonas();
        if (personasData) {
            setPersonas(personasData);
        }
        setIsLoading(false);
    };

    return (
        <div style={{ marginBottom: '20px' }}>
            <button onClick={handleStartDebate} disabled={isLoading || debateStarted}>Start Debate</button>
            {debateStarted && (
                <>
                    <button onClick={handleOneTurnDebate} disabled={isLoading} style={{ marginLeft: '10px' }}>One Turn Debate</button>
                    <button onClick={handleGetPersonas} disabled={isLoading} style={{ marginLeft: '10px' }}>Get Personas</button>
                    <label style={{ marginLeft: '10px' }}>
                        <input
                            type="checkbox"
                            checked={useWebSocket}
                            onChange={() => setUseWebSocket(!useWebSocket)}
                        />
                        Use WebSocket
                    </label>
                </>
            )}
            {isLoading && <p>Loading...</p>}
        </div>
    );
};

export default DebateController;