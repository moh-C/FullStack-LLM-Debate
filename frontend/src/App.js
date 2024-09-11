import React, { useState } from "react";
import ApiTestDashboard from "./components/ApiTestDashboard";
import DebateController from "./components/DebateController";
import DebateDisplay from "./components/DebateDisplay";
import PersonaDisplay from "./components/PersonaDisplay";

const App = () => {
  const [debateStarted, setDebateStarted] = useState(false);
  const [debateResponses, setDebateResponses] = useState([]);
  const [personas, setPersonas] = useState(null);

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-8">
      <h1 className="text-4xl font-bold mb-8 text-blue-400">
        Debate API Dashboard
      </h1>

      <div className="space-y-8">
        <ApiTestDashboard />
        <DebateController
          debateStarted={debateStarted}
          setDebateStarted={setDebateStarted}
          setDebateResponses={setDebateResponses}
          setPersonas={setPersonas}
        />
        {debateStarted && <DebateDisplay debateResponses={debateResponses} />}
        {personas && <PersonaDisplay personas={personas} />}
      </div>
    </div>
  );
};

export default App;
