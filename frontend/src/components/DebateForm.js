import React, { useState } from "react";

const DebateForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    topic: "Costco Muffins",
    name1: "Kevin Hart",
    name2: "Justin Bieber",
    question: "Why are they so big?",
    provider: "openai",
    answer_length: 200,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: name === "answer_length" ? parseInt(value, 10) : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label
          htmlFor="topic"
          className="block text-sm font-medium text-gray-300"
        >
          Debate Topic:
        </label>
        <input
          type="text"
          id="topic"
          name="topic"
          value={formData.topic}
          onChange={handleChange}
          required
          className="mt-1 block w-full bg-gray-700 border border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>
      <div>
        <label
          htmlFor="name1"
          className="block text-sm font-medium text-gray-300"
        >
          Debater 1 Name:
        </label>
        <input
          type="text"
          id="name1"
          name="name1"
          value={formData.name1}
          onChange={handleChange}
          required
          className="mt-1 block w-full bg-gray-700 border border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>
      <div>
        <label
          htmlFor="name2"
          className="block text-sm font-medium text-gray-300"
        >
          Debater 2 Name:
        </label>
        <input
          type="text"
          id="name2"
          name="name2"
          value={formData.name2}
          onChange={handleChange}
          required
          className="mt-1 block w-full bg-gray-700 border border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>
      <div>
        <label
          htmlFor="question"
          className="block text-sm font-medium text-gray-300"
        >
          Initial Question:
        </label>
        <input
          type="text"
          id="question"
          name="question"
          value={formData.question}
          onChange={handleChange}
          required
          className="mt-1 block w-full bg-gray-700 border border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>
      <div>
        <label
          htmlFor="provider"
          className="block text-sm font-medium text-gray-300"
        >
          Provider:
        </label>
        <select
          id="provider"
          name="provider"
          value={formData.provider}
          onChange={handleChange}
          required
          className="mt-1 block w-full bg-gray-700 border border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        >
          <option value="openai">OpenAI</option>
          <option value="claude">Claude</option>
        </select>
      </div>
      <div>
        <label
          htmlFor="answer_length"
          className="block text-sm font-medium text-gray-300"
        >
          Answer Length:
        </label>
        <input
          type="number"
          id="answer_length"
          name="answer_length"
          value={formData.answer_length}
          onChange={handleChange}
          min="100"
          max="1000"
          required
          className="mt-1 block w-full bg-gray-700 border border-gray-600 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />
      </div>
      <button
        type="submit"
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        Start Debate
      </button>
    </form>
  );
};

export default DebateForm;
