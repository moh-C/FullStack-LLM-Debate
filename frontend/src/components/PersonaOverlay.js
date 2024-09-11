import React from 'react';
import PersonaCard from './PersonaCard';

const PersonaOverlay = ({ onClose }) => {
    // Mock data for personas
    const mockPersonas = [
        { id: 1, name1: "Einstein", name2: "Newton", provider: "openai", answer_length: 150 },
        { id: 2, name1: "Shakespeare", name2: "Hemingway", provider: "claude", answer_length: 200 },
        { id: 3, name1: "Socrates", name2: "Plato", provider: "openai", answer_length: 180 },
        { id: 4, name1: "Tesla", name2: "Edison", provider: "claude", answer_length: 220 },
        { id: 5, name1: "Curie", name2: "Bohr", provider: "openai", answer_length: 190 },
        { id: 6, name1: "Da Vinci", name2: "Michelangelo", provider: "claude", answer_length: 170 }
    ];

    const handlePersonaSelect = (persona) => {
        console.log("Selected persona:", persona);
        onClose();
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-8 max-w-4xl max-h-[80vh] overflow-y-auto">
                <h2 className="text-2xl font-bold mb-4">Persona History</h2>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {mockPersonas.map((persona) => (
                        <PersonaCard
                            key={persona.id}
                            persona={persona}
                            onSelect={handlePersonaSelect}
                        />
                    ))}
                </div>
                <button
                    onClick={onClose}
                    className="mt-6 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                >
                    Close
                </button>
            </div>
        </div>
    );
};

export default PersonaOverlay;