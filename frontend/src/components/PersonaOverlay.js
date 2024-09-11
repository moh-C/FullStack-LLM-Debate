import React, { useContext } from 'react';
import { DebateContext } from '../contexts/DebateContext';
import PersonaCard from './PersonaCard';

const PersonaOverlay = ({ onClose }) => {
    const { personas, handlePersonaSelect } = useContext(DebateContext);

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-8 max-w-4xl max-h-[80vh] overflow-y-auto">
                <h2 className="text-2xl font-bold mb-4">Persona History</h2>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {personas.map((persona) => (
                        <PersonaCard
                            key={persona.id}
                            persona={persona}
                            onSelect={(selectedPersona) => {
                                handlePersonaSelect(selectedPersona);
                                onClose();
                            }}
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