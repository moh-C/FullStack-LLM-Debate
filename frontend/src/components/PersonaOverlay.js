import React, { useState, useEffect } from 'react';
import PersonaCard from './PersonaCard';
import { getPersonas } from '../utils/api';

const PersonaOverlay = ({ onClose }) => {
    const [personas, setPersonas] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPersonas = async () => {
            setIsLoading(true);
            try {
                const fetchedPersonas = await getPersonas();

                // Get unique personas based on name1 and name2 combination
                const uniquePersonas = fetchedPersonas.filter((persona, index, self) =>
                    index === self.findIndex((t) => (
                        t.name1 === persona.name1 && t.name2 === persona.name2
                    ))
                );

                // Boilerplate personas
                const boilerplatePersonas = [
                    { id: 'bp1', name1: "Pete Davidson", name2: "Shaq O'Neal", topic: "Best fast food chain", answer_length: 150 },
                    { id: 'bp2', name1: "Max Verstappen", name2: "Joe Biden", topic: "Future of transportation", answer_length: 200 },
                    { id: 'bp3', name1: "Justin Bieber", name2: "Pete Davidson", topic: "Social media influence", answer_length: 180 },
                    { id: 'bp4', name1: "Shaq O'Neal", name2: "Max Verstappen", topic: "Importance of sports", answer_length: 220 },
                    { id: 'bp5', name1: "Joe Biden", name2: "Justin Bieber", topic: "Climate change solutions", answer_length: 190 },
                    { id: 'bp6', name1: "Pete Davidson", name2: "Max Verstappen", topic: "Celebrity culture", answer_length: 170 }
                ];

                setPersonas([...uniquePersonas, ...boilerplatePersonas]);
            } catch (err) {
                setError('Failed to fetch personas');
                console.error(err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchPersonas();
    }, []);

    const handlePersonaSelect = (persona) => {
        if (persona.persona1_system_prompt) {
            console.log("Persona 1 System Prompt:", persona.persona1_system_prompt);
            console.log("Persona 2 System Prompt:", persona.persona2_system_prompt);
        } else {
            console.log("Boilerplate persona selected:", persona);
        }
        onClose();
    };

    if (isLoading) return <div className="text-center">Loading personas...</div>;
    if (error) return <div className="text-center text-red-500">{error}</div>;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-8 w-full max-w-4xl max-h-[80vh] overflow-y-auto">
                <h2 className="text-2xl font-bold mb-4">Persona History</h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {personas.map((persona, index) => (
                        <React.Fragment key={persona.id}>
                            {index === personas.length - 6 && (
                                <div className="col-span-full my-6 flex items-center">
                                    <div className="flex-grow border-t border-gray-300"></div>
                                    <span className="flex-shrink mx-4 text-gray-400">Suggestions</span>
                                    <div className="flex-grow border-t border-gray-300"></div>
                                </div>
                            )}
                            <PersonaCard
                                persona={persona}
                                onSelect={handlePersonaSelect}
                            />
                        </React.Fragment>
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