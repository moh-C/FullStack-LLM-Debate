import React from "react";

const PersonaDisplay = ({ personas }) => {
  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold mb-4 text-blue-400">Personas</h2>
      <div className="space-y-6">
        <div className="bg-gray-700 p-4 rounded-lg">
          <h3 className="text-xl font-medium text-purple-400 mb-2">
            Persona 1: {personas.persona1.name}
          </h3>
          <p className="text-gray-300 whitespace-pre-wrap">
            {personas.persona1.system_prompt}
          </p>
        </div>
        <div className="bg-gray-700 p-4 rounded-lg">
          <h3 className="text-xl font-medium text-green-400 mb-2">
            Persona 2: {personas.persona2.name}
          </h3>
          <p className="text-gray-300 whitespace-pre-wrap">
            {personas.persona2.system_prompt}
          </p>
        </div>
      </div>
    </div>
  );
};

export default PersonaDisplay;
