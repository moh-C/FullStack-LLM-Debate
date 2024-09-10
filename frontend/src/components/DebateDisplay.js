import React from 'react';

const DebateDisplay = ({ debateResponses }) => {
    return (
        <div>
            <h2>Debate Progress</h2>
            <div style={{
                border: '1px solid #ccc',
                padding: '10px',
                maxHeight: '400px',
                overflowY: 'auto'
            }}>
                {debateResponses.map((response, index) => (
                    <p key={index}><strong>{response.name}:</strong> {response.response}</p>
                ))}
            </div>
        </div>
    );
};

export default DebateDisplay;