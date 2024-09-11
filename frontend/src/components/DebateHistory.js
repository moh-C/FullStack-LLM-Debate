import React from 'react';

const DebateHistory = () => {
    // Mock data for debates
    const mockDebates = [
        { id: 1, topic: "Climate Change Solutions", question: "How can we effectively reduce carbon emissions?" },
        { id: 2, topic: "Artificial Intelligence Ethics", question: "Should AI development be regulated?" },
        { id: 3, topic: "Space Exploration", question: "Is colonizing Mars a viable goal for humanity?" },
        { id: 4, topic: "Cryptocurrency Future", question: "Will cryptocurrencies replace traditional banking?" },
        { id: 5, topic: "Renewable Energy", question: "Can renewable energy fully replace fossil fuels by 2050?" }
    ];

    return (
        <div className="w-1/6 bg-white shadow-md overflow-y-auto">
            <h2 className="text-xl font-semibold p-4 border-b">Debate History</h2>
            <ul>
                {mockDebates.map((debate) => (
                    <li
                        key={debate.id}
                        className="p-3 hover:bg-gray-100 cursor-pointer"
                    >
                        <h3 className="font-medium">{debate.topic}</h3>
                        <p className="text-sm text-gray-600">{debate.question}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default DebateHistory;