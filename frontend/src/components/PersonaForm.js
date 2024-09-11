import React, { useContext } from 'react';
import { DebateContext } from '../contexts/DebateContext';

const PersonaForm = () => {
    const { formData, setFormData, handleSubmit } = useContext(DebateContext);

    const handleInputChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return (
        <form onSubmit={handleSubmit} className="p-4 space-y-4">
            <input
                name="topic"
                value={formData.topic}
                onChange={handleInputChange}
                placeholder="Debate Topic"
                className="w-full p-2 rounded border"
            />
            <input
                name="name1"
                value={formData.name1}
                onChange={handleInputChange}
                placeholder="Debater 1 Name"
                className="w-full p-2 rounded border"
            />
            <input
                name="name2"
                value={formData.name2}
                onChange={handleInputChange}
                placeholder="Debater 2 Name"
                className="w-full p-2 rounded border"
            />
            <input
                name="question"
                value={formData.question}
                onChange={handleInputChange}
                placeholder="Initial Question"
                className="w-full p-2 rounded border"
            />
            <select
                name="provider"
                value={formData.provider}
                onChange={handleInputChange}
                className="w-full p-2 rounded border"
            >
                <option value="openai">OpenAI</option>
                <option value="claude">Claude</option>
            </select>
            <input
                type="number"
                name="answer_length"
                value={formData.answer_length}
                onChange={handleInputChange}
                placeholder="Answer Length"
                className="w-full p-2 rounded border"
            />
            <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded">
                Start Debate
            </button>
        </form>
    );
};

export default PersonaForm;