import React, { useState } from 'react';

const DebateForm = ({ onSubmit }) => {
    const [formData, setFormData] = useState({
        topic: 'Costco Muffins',
        name1: 'Kevin Hart',
        name2: 'Justin Bieber',
        question: 'Why are they so big?',
        provider: 'openai',
        answer_length: 200
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevData => ({
            ...prevData,
            [name]: name === 'answer_length' ? parseInt(value, 10) : value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="topic">Debate Topic:</label>
                <input
                    type="text"
                    id="topic"
                    name="topic"
                    value={formData.topic}
                    onChange={handleChange}
                    required
                />
            </div>
            <div>
                <label htmlFor="name1">Debater 1 Name:</label>
                <input
                    type="text"
                    id="name1"
                    name="name1"
                    value={formData.name1}
                    onChange={handleChange}
                    required
                />
            </div>
            <div>
                <label htmlFor="name2">Debater 2 Name:</label>
                <input
                    type="text"
                    id="name2"
                    name="name2"
                    value={formData.name2}
                    onChange={handleChange}
                    required
                />
            </div>
            <div>
                <label htmlFor="question">Initial Question:</label>
                <input
                    type="text"
                    id="question"
                    name="question"
                    value={formData.question}
                    onChange={handleChange}
                    required
                />
            </div>
            <div>
                <label htmlFor="provider">Provider:</label>
                <select
                    id="provider"
                    name="provider"
                    value={formData.provider}
                    onChange={handleChange}
                    required
                >
                    <option value="openai">OpenAI</option>
                    <option value="claude">Claude</option>
                </select>
            </div>
            <div>
                <label htmlFor="answer_length">Answer Length:</label>
                <input
                    type="number"
                    id="answer_length"
                    name="answer_length"
                    value={formData.answer_length}
                    onChange={handleChange}
                    min="100"
                    max="1000"
                    required
                />
            </div>
            <button type="submit">Start Debate</button>
        </form>
    );
};

export default DebateForm;