import React, { useEffect, useRef } from "react";
import { UserCircle } from "lucide-react";

const DebateDisplay = ({ debateResponses }) => {
  const displayRef = useRef(null);

  useEffect(() => {
    if (displayRef.current) {
      displayRef.current.scrollTop = displayRef.current.scrollHeight;
    }
  }, [debateResponses]);

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold mb-4 text-blue-400">
        Debate Progress
      </h2>
      <div
        ref={displayRef}
        className="bg-gray-700 p-4 rounded-lg max-h-96 overflow-y-auto space-y-6"
      >
        {debateResponses.map((response, index) => (
          <div
            key={index}
            className={`flex items-start ${
              index % 2 === 0 ? "justify-start" : "justify-end"
            }`}
          >
            <div
              className={`flex items-start ${
                index % 2 === 0 ? "w-3/4" : "w-5/6"
              }`}
            >
              <div
                className={`flex-shrink-0 ${
                  index % 2 === 0 ? "mr-3" : "ml-3 order-last"
                }`}
              >
                <UserCircle
                  size={40}
                  className={
                    index % 2 === 0 ? "text-purple-400" : "text-green-400"
                  }
                />
              </div>
              <div
                className={`flex-grow bg-gray-600 p-3 rounded ${
                  index % 2 === 0 ? "rounded-tl-none" : "rounded-tr-none"
                }`}
              >
                <strong
                  className={`${
                    index % 2 === 0 ? "text-purple-300" : "text-green-300"
                  }`}
                >
                  {response.name}:
                </strong>
                <p className="mt-1 text-gray-200">{response.response}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DebateDisplay;
