import React, { useContext } from 'react';
import { DebateContext } from '../contexts/DebateContext';
import { UserCircle, Send } from 'lucide-react';

const ChatArea = () => {
    const { currentDebate } = useContext(DebateContext);

    return (
        <div className="flex-1 flex flex-col">
            {currentDebate ? (
                <>
                    <div className="flex-1 overflow-y-auto p-4 space-y-4">
                        {currentDebate.turns.map((turn, index) => (
                            <div
                                key={index}
                                className={`flex items-start ${index % 2 === 0 ? 'justify-start' : 'justify-end'
                                    }`}
                            >
                                <div className={`flex items-start max-w-3/4 ${index % 2 === 0 ? 'flex-row' : 'flex-row-reverse'
                                    }`}>
                                    <UserCircle
                                        size={40}
                                        className={index % 2 === 0 ? 'text-blue-500' : 'text-green-500'}
                                    />
                                    <div className={`mx-2 p-3 rounded-lg ${index % 2 === 0 ? 'bg-blue-100' : 'bg-green-100'
                                        }`}>
                                        <p className="text-gray-800">{turn.content}</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                    <div className="p-4 border-t">
                        <form className="flex items-center">
                            <input
                                type="text"
                                placeholder="Type a message..."
                                className="flex-1 p-2 rounded-l-lg border"
                            />
                            <button className="bg-blue-500 text-white p-2 rounded-r-lg">
                                <Send size={20} />
                            </button>
                        </form>
                    </div>
                </>
            ) : (
                <div className="flex-1 flex items-center justify-center text-gray-500">
                    Select a debate or start a new one
                </div>
            )}
        </div>
    );
};

export default ChatArea;