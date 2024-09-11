import React, { useState } from "react";
import { testEndpoint } from "../utils/api";

const ApiTestDashboard = () => {
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleTestEndpoint = async (endpoint) => {
    setIsLoading(true);
    const response = await testEndpoint(endpoint);
    setMessage(JSON.stringify(response, null, 2));
    setIsLoading(false);
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold mb-4 text-blue-400">
        API Test Dashboard
      </h2>
      <div className="space-x-4 mb-4">
        <button
          onClick={() => handleTestEndpoint("/")}
          disabled={isLoading}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
        >
          Test Root
        </button>
        <button
          onClick={() => handleTestEndpoint("/health")}
          disabled={isLoading}
          className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
        >
          Test Health
        </button>
      </div>
      {isLoading ? (
        <p className="text-yellow-400">Loading...</p>
      ) : (
        <pre className="bg-gray-700 p-4 rounded-lg overflow-x-auto text-sm">
          {message || "No message yet. Click a button to test an endpoint."}
        </pre>
      )}
    </div>
  );
};

export default ApiTestDashboard;
