import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const ReviewAssessment = () => {
    const { state } = useLocation();
    const { questions, selectedOptions, timeSpentPerQuestion } = state;
    const navigate = useNavigate();

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-6">Review Your Assessment</h1>
            <div className="bg-gray-200 p-4 rounded shadow">
                <ul className="list-none">
                    {questions.map((question, index) => {
                        const userAnswer = question.options[selectedOptions[index]] || 'Not answered';
                        const isCorrect = userAnswer === question.answer;

                        return (
                            <li key={index} className="mb-4 p-4 border border-gray-300 rounded">
                                <h2 className="font-semibold">Q{index + 1}: {question.question}</h2>
                                <p className="text-gray-600">Time Spent: {timeSpentPerQuestion[index] / 1000.0} seconds</p>
                                <p className="text-gray-600">Your Answer: {userAnswer}</p>
                                <p className="text-gray-800">Correct Answer: {question.answer}</p>
                                <p className={`font-bold ${isCorrect ? 'text-green-500' : 'text-red-500'}`}>
                                    {isCorrect ? 'Correct' : 'Incorrect'}
                                </p>
                            </li>
                        );
                    })}
                </ul>
            </div>

            {/* Buttons Section */}
            <div className="flex mt-6">
                <button
                    className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                    onClick={() => navigate('/')}
                >
                    Attempt Another Quiz
                </button>
            
            </div>
        </div>
    );
};

export default ReviewAssessment;
