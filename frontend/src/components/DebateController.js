import React, { useState, useEffect, useRef } from 'react';
import { startDebate, oneTurnDebate, getPersonas } from '../utils/api';
import DebateForm from './DebateForm';

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
                    setDebateResponses(prev => {
                        const lastResponse = prev[prev.length - 1];
                        if (lastResponse && lastResponse.name === data.name) {
                            return [
                                ...prev.slice(0, -1),
                                { ...lastResponse, response: lastResponse.response + data.chunk }
                            ];
                        } else {
                            return [...prev, { name: data.name, response: data.chunk }];
                        }
                    });
                }
            };
            return () => {
                if (ws.current) {
                    ws.current.close();
                }
            };
        }
    }, [debateStarted, useWebSocket, setDebateResponses]);

    const handleStartDebate = async (formData) => {
        setIsLoading(true);
        const debateData = {
            topic: formData.topic,
            name1: formData.name1,
            name2: formData.name2,
            questions: [formData.question],
            provider: formData.provider,
            answer_length: formData.answer_length
        };
        const success = await startDebate(debateData);
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
            {!debateStarted ? (
                <DebateForm onSubmit={handleStartDebate} />
            ) : (
                <>
                    <button onClick={handleOneTurnDebate} disabled={isLoading} style={{ marginRight: '10px' }}>
                        One Turn Debate
                    </button>
                    <button onClick={handleGetPersonas} disabled={isLoading} style={{ marginRight: '10px' }}>
                        Get Personas
                    </button>
                    <label>
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