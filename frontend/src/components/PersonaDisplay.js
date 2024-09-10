import React from 'react';

const PersonaDisplay = ({ personas }) => {
    return (
        <div>
            <h2>Personas</h2>
            <div style={{
                border: '1px solid #ccc',
                padding: '10px',
                maxHeight: '400px',
                overflowY: 'auto'
            }}>
                <h3>Persona 1: {personas.persona1.name}</h3>
                <p>{personas.persona1.system_prompt}</p>
                <h3>Persona 2: {personas.persona2.name}</h3>
                <p>{personas.persona2.system_prompt}</p>
            </div>
        </div>
    );
};

export default PersonaDisplay;