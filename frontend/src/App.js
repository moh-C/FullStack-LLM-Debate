import React, { useState } from 'react';
import ApiTestDashboard from './components/ApiTestDashboard';
import DebateController from './components/DebateController';
import DebateDisplay from './components/DebateDisplay';
import PersonaDisplay from './components/PersonaDisplay';

const App = () => {
    const [debateStarted, setDebateStarted] = useState(false);
    const [debateResponses, setDebateResponses] = useState([]);
    const [personas, setPersonas] = useState(null);

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
            <h1>Debate API Dashboard</h1>
            <ApiTestDashboard />
            <DebateController
                debateStarted={debateStarted}
                setDebateStarted={setDebateStarted}
                setDebateResponses={setDebateResponses}
                setPersonas={setPersonas}
            />
            {debateStarted && (
                <DebateDisplay debateResponses={debateResponses} />
            )}
            {personas && (
                <PersonaDisplay personas={personas} />
            )}
        </div>
    );
};

export default App;