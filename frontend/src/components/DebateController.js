import React, { useState, useEffect, useRef } from "react";
import { startDebate, oneTurnDebate, getPersonas } from "../utils/api";
import DebateForm from "./DebateForm";

const DebateController = ({
  debateStarted,
  setDebateStarted,
  setDebateResponses,
  setPersonas,
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [useWebSocket, setUseWebSocket] = useState(true);
  const ws = useRef(null);

  useEffect(() => {
    if (debateStarted && useWebSocket) {
      ws.current = new WebSocket("ws://localhost:8000/ws");
      ws.current.onmessage = (event) => {
        if (event.data === "<END_WEBSOCKET_TOKEN>") {
          setIsLoading(false);
        } else {
          const data = JSON.parse(event.data);
          setDebateResponses((prev) => {
            const lastResponse = prev[prev.length - 1];
            if (lastResponse && lastResponse.name === data.name) {
              return [
                ...prev.slice(0, -1),
                {
                  ...lastResponse,
                  response: lastResponse.response + data.chunk,
                },
              ];
            } else {
              return [...prev, { name: data.name, response: data.chunk }];
            }
          });
        }
      };
      return () => {
        if (ws.current) {
          ws.current.close();
        }
      };
    }
  }, [debateStarted, useWebSocket, setDebateResponses]);

  const handleStartDebate = async (formData) => {
    setIsLoading(true);
    const debateData = {
      topic: formData.topic,
      name1: formData.name1,
      name2: formData.name2,
      questions: [formData.question],
      provider: formData.provider,
      answer_length: formData.answer_length,
    };
    const success = await startDebate(debateData);
    if (success) {
      setDebateStarted(true);
    }
    setIsLoading(false);
  };

  const handleOneTurnDebate = async () => {
    setIsLoading(true);
    if (useWebSocket && ws.current) {
      ws.current.send("next");
    } else {
      const response = await oneTurnDebate();
      if (response) {
        setDebateResponses((prev) => [...prev, response]);
      }
      setIsLoading(false);
    }
  };

  const handleGetPersonas = async () => {
    setIsLoading(true);
    const personasData = await getPersonas();
    if (personasData) {
      setPersonas(personasData);
    }
    setIsLoading(false);
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold mb-4 text-blue-400">
        Debate Controller
      </h2>
      {!debateStarted ? (
        <DebateForm onSubmit={handleStartDebate} />
      ) : (
        <div className="space-y-4">
          <button
            onClick={handleOneTurnDebate}
            disabled={isLoading}
            className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
          >
            One Turn Debate
          </button>
          <button
            onClick={handleGetPersonas}
            disabled={isLoading}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
          >
            Get Personas
          </button>
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={useWebSocket}
              onChange={() => setUseWebSocket(!useWebSocket)}
              className="form-checkbox text-blue-600"
            />
            <span>Use WebSocket</span>
          </label>
        </div>
      )}
      {isLoading && <p className="text-yellow-400 mt-4">Loading...</p>}
    </div>
  );
};

export default DebateController;
