import React, { useEffect, useRef } from 'react';

const DebateDisplay = ({ debateResponses }) => {
    const displayRef = useRef(null);

    useEffect(() => {
        if (displayRef.current) {
            displayRef.current.scrollTop = displayRef.current.scrollHeight;
        }
    }, [debateResponses]);

    return (
        <div>
            <h2>Debate Progress</h2>
            <div
                ref={displayRef}
                style={{
                    border: '1px solid #ccc',
                    padding: '10px',
                    maxHeight: '400px',
                    overflowY: 'auto'
                }}
            >
                {debateResponses.map((response, index) => (
                    <p key={index}>
                        <strong>{response.name}:</strong> {response.response}
                    </p>
                ))}
            </div>
        </div>
    );
};

export default DebateDisplay;