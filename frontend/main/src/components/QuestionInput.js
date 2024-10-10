import React, { useState } from 'react';

const QuestionInput = () => {
  const [numQuestions, setNumQuestions] = useState('');

  const handleInputChange = (event) => {
    const inputValue = event.target.value;
    setNumQuestions(inputValue);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle the submission or further processing here
    console.log('Number of questions selected:', numQuestions);
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Enter Number of Questions</h2>
      <form onSubmit={handleSubmit} className="flex items-center space-x-2">
        <label htmlFor="numQuestionsInput" className="text-gray-700">
          Questions:
        </label>
        <input
          type="number"
          id="numQuestionsInput"
          className="p-2 border rounded-md"
          value={numQuestions}
          onChange={handleInputChange}
        />
        <button
          type="submit"
          className="p-2 bg-blue-500 text-white rounded-md cursor-pointer"
        >
          Submit
        </button>
      </form>
    </div>
  );
};

export default QuestionInput;
