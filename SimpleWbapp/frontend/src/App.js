import React, { useState } from 'react';

function App() {
    const [input, setInput] = useState('');
    const [output, setOutput] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleGenerate = async () => {
        setIsLoading(true);
        setOutput('');

        const eventSource = new EventSource('http://localhost:8000/stream');

        eventSource.onmessage = function (event) {
            if (event.data === '[DONE]') {
                eventSource.close();
                setIsLoading(false);
            } else {
                setOutput(prevOutput => prevOutput + event.data);
            }
        };

        eventSource.onerror = function (error) {
            console.error('EventSource failed:', error);
            eventSource.close();
            setIsLoading(false);
        };
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">LLM Interface</h1>
            <div className="mb-4">
                <textarea
                    className="w-full p-2 border rounded"
                    rows="4"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Enter your prompt here..."
                />
            </div>
            <button
                className="bg-blue-500 text-white px-4 py-2 rounded"
                onClick={handleGenerate}
                disabled={isLoading}
            >
                {isLoading ? 'Generating...' : 'Generate'}
            </button>
            <div className="mt-4">
                <h2 className="text-xl font-semibold mb-2">Output:</h2>
                <div className="border p-2 rounded min-h-[100px] whitespace-pre-wrap">
                    {output || 'Output will appear here...'}
                </div>
            </div>
        </div>
    );
}

export default App;