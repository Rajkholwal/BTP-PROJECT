import React from 'react';
import { useLocation } from 'react-router-dom';

const ReviewAssessment = () => {
    const { state } = useLocation();
    const { questions, marks, seconds } = state;

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-6">Review Your Assessment</h1>
            
            <div className="bg-gray-200 p-4 rounded shadow">
                <ul className="list-none">
                    {questions.map((question, index) => (
                        <li key={index} className="mb-4 p-4 border border-gray-300 rounded">
                            <h2 className="font-semibold">Q{index + 1}: {question.question}</h2>
                            <p className="text-gray-600">Time Spent: {seconds[index]} seconds</p>
                            <p className="text-gray-800">Your Answer: {question.selectedAnswer}</p>
                            <p className="text-gray-800">Correct Answer: {question.correctAnswer}</p>
                            <p className={`font-bold ${question.selectedAnswer === question.correctAnswer ? 'text-green-500' : 'text-red-500'}`}>
                                {question.selectedAnswer === question.correctAnswer ? 'Correct' : 'Incorrect'}
                            </p>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default ReviewAssessment;
