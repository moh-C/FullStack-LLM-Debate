import React from 'react';

const PersonaCard = ({ persona, onSelect }) => {
    return (
        <div
            onClick={() => onSelect(persona)}
            className="bg-white rounded-lg shadow-lg overflow-hidden transform transition duration-500 hover:scale-105 cursor-pointer"
        >
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-4">
                <h3 className="text-xl font-bold text-white">{persona.name1} vs {persona.name2}</h3>
            </div>
            <div className="p-4">
                <p className="text-gray-600">Provider: {persona.provider}</p>
                <p className="text-gray-600">Answer Length: {persona.answer_length}</p>
            </div>
        </div>
    );
};

export default PersonaCard;