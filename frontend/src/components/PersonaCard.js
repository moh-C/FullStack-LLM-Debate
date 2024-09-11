import React from 'react';

const PersonaCard = ({ persona, onSelect }) => {
    return (
        <div
            onClick={() => onSelect(persona)}
            className="bg-white rounded-lg shadow-lg overflow-hidden transform transition duration-500 hover:scale-105 cursor-pointer flex flex-col h-full"
        >
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-4 flex-grow flex flex-col items-center justify-center text-center">
                <h3 className="text-xl font-bold text-white">{persona.name1}</h3>
                <p className="text-white text-lg my-1">vs</p>
                <h3 className="text-xl font-bold text-white">{persona.name2}</h3>
            </div>
            <div className="p-4 text-center">
                <p className="text-gray-800 font-semibold mb-2">{persona.topic}</p>
                <p className="text-gray-600">Answer Length: {persona.answer_length}</p>
            </div>
        </div>
    );
};

export default PersonaCard;