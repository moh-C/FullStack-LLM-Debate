import React, { useState } from 'react';
import DebateHistory from './components/DebateHistory';
import ChatArea from './components/ChatArea';
import PersonaForm from './components/PersonaForm';
import PersonaOverlay from './components/PersonaOverlay';
import { DebateProvider } from './contexts/DebateContext';

const App = () => {
  const [showPersonaOverlay, setShowPersonaOverlay] = useState(false);

  return (
    <DebateProvider>
      <div className="flex h-screen bg-gray-100">
        <DebateHistory />
        <ChatArea />
        <div className="w-1/6 bg-white shadow-md overflow-y-auto">
          <PersonaForm />
          <button
            onClick={() => setShowPersonaOverlay(true)}
            className="w-full bg-blue-500 text-white p-2 mt-4"
          >
            View Persona History
          </button>
        </div>
      </div>
      {showPersonaOverlay && (
        <PersonaOverlay onClose={() => setShowPersonaOverlay(false)} />
      )}
    </DebateProvider>
  );
};

export default App;