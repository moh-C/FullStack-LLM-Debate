import React, { useState } from 'react';
import { ChevronRight, Loader2 } from 'lucide-react';

function App() {
    const [input, setInput] = useState('');
    const [output, setOutput] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleGenerate = async () => {
        setIsLoading(true);
        setOutput('');

        const eventSource = new EventSource(`http://localhost:8000/generate?prompt=${encodeURIComponent(input)}`);

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
        <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
            <div className="relative py-3 sm:max-w-xl sm:mx-auto">
                <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-light-blue-500 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
                <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
                    <div className="max-w-md mx-auto">
                        <div>
                            <h1 className="text-2xl font-semibold text-gray-900">AI Assistant</h1>
                        </div>
                        <div className="divide-y divide-gray-200">
                            <div className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                                <div className="flex flex-col">
                                    <label className="leading-loose">Your Prompt</label>
                                    <textarea
                                        className="px-4 py-2 border focus:ring-gray-500 focus:border-gray-900 w-full sm:text-sm border-gray-300 rounded-md focus:outline-none text-gray-600"
                                        rows="4"
                                        value={input}
                                        onChange={(e) => setInput(e.target.value)}
                                        placeholder="Enter your prompt here..."
                                    />
                                </div>
                                <div className="pt-4 flex items-center space-x-4">
                                    <button
                                        className="bg-blue-500 flex justify-center items-center w-full text-white px-4 py-3 rounded-md focus:outline-none"
                                        onClick={handleGenerate}
                                        disabled={isLoading}
                                    >
                                        {isLoading ? (
                                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                        ) : (
                                            <ChevronRight className="mr-2 h-4 w-4" />
                                        )}
                                        {isLoading ? 'Generating...' : 'Generate'}
                                    </button>
                                </div>
                            </div>
                            <div className="pt-6 text-base leading-6 font-bold sm:text-lg sm:leading-7">
                                <p className="text-gray-900">Output:</p>
                                <div className="mt-2 text-gray-600 whitespace-pre-wrap">
                                    {output || 'Your response will appear here...'}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;