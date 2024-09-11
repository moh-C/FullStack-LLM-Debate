import React, { createContext, useState, useEffect } from 'react';
import { fetchDebateHistory, fetchPersonas, startDebate } from '../utils/api';

export const DebateContext = createContext();

export const DebateProvider = ({ children }) => {
    const [debates, setDebates] = useState([]);
    const [currentDebate, setCurrentDebate] = useState(null);
    const [personas, setPersonas] = useState([]);
    const [formData, setFormData] = useState({
        topic: '',
        name1: '',
        name2: '',
        question: '',
        provider: 'openai',
        answer_length: 200,
    });

    useEffect(() => {
        fetchDebateHistory().then(setDebates);
        fetchPersonas().then(setPersonas);
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const newDebate = await startDebate(formData);
        if (newDebate) {
            setDebates([...debates, newDebate]);
            setCurrentDebate(newDebate);
        }
    };

    const handlePersonaSelect = (persona) => {
        setFormData({
            ...formData,
            name1: persona.name1,
            name2: persona.name2,
            provider: persona.provider,
            answer_length: persona.answer_length,
        });
    };

    return (
        <DebateContext.Provider
            value={{
                debates,
                setDebates,
                currentDebate,
                setCurrentDebate,
                personas,
                setPersonas,
                formData,
                setFormData,
                handleSubmit,
                handlePersonaSelect,
            }}
        >
            {children}
        </DebateContext.Provider>
    );
};