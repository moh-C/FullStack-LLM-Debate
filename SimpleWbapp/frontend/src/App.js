import React, { useState, useCallback } from 'react';

function App() {
    const [input, setInput] = useState('');
    const [output, setOutput] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleGenerate = useCallback(async () => {
        setIsLoading(true);
        setOutput('');

        try {
            const response = await fetch('http://localhost:8000/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: input }),
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            let buffer = '';
            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');

                buffer = lines.pop() || '';

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6);
                        if (data === '[DONE]') {
                            setIsLoading(false);
                        } else {
                            setOutput(prevOutput => prevOutput + data);
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Error:', error);
            setOutput('An error occurred while generating the response.');
        } finally {
            setIsLoading(false);
        }
    }, [input]);

    return (
        <div className="container">
            <h1>AI Assistant</h1>
            <div>
                <label htmlFor="prompt">Your Prompt</label>
                <textarea
                    id="prompt"
                    rows="4"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Enter your prompt here..."
                />
            </div>
            <button onClick={handleGenerate} disabled={isLoading}>
                {isLoading ? 'Generating...' : 'Generate'}
            </button>
            <div>
                <h2>Output:</h2>
                <pre>{output || 'Your response will appear here...'}</pre>
            </div>
        </div>
    );
}

export default App;