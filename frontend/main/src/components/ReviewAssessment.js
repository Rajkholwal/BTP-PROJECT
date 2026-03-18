import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const ReviewAssessment = () => {
    const { state } = useLocation();
    const { questions, selectedOptions, timeSpentPerQuestion } = state;
    console.log("review",questions);
    const navigate = useNavigate();

    const formatTime = (milliseconds = 0) => {
        const totalSeconds = Math.floor(milliseconds / 1000);
        const minutes = Math.floor(totalSeconds / 60);
        const seconds = totalSeconds % 60;
        return `${minutes}:${String(seconds).padStart(2, '0')}`;
    };

    const totalTimeMs = (timeSpentPerQuestion || []).reduce((sum, x) => sum + (x || 0), 0);

    return (
        <div className="container mx-auto p-4">
            <div className="mx-auto max-w-5xl">
                <div className="mb-4 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
                    <div>
                        <h1 className="text-3xl font-bold mb-1">Review Your Assessment</h1>
                        <p className="text-sm text-slate-600">
                            Total time: <span className="font-semibold text-slate-900">{formatTime(totalTimeMs)}</span>
                        </p>
                    </div>
                    <button
                        className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
                        onClick={() => navigate('/')}
                    >
                        Attempt Another Quiz
                    </button>
                </div>

                <div className="bg-white p-4 rounded-xl border border-gray-200 shadow">
                    <ul className="list-none">
                        {questions.map((question, index) => {
                            const userAnswer = question.options[selectedOptions[index]] || 'Not answered';
                            const isCorrect = userAnswer === question.answer;

                            return (
                                <li key={index} className="mb-4 p-4 border border-gray-200 rounded">
                                    <h2 className="font-semibold">Q{index + 1}: {question.question}</h2>
                                    <div className="mt-2 grid gap-1 text-sm">
                                        <p className="text-slate-600">
                                            Time Spent:{' '}
                                            <span className="font-semibold text-slate-900">{formatTime(timeSpentPerQuestion?.[index] || 0)}</span>
                                        </p>
                                        <p className="text-slate-600">Your Answer: <span className="font-semibold text-slate-900">{userAnswer}</span></p>
                                        <p className="text-slate-600">Correct Answer: <span className="font-semibold text-slate-900">{question.answer}</span></p>
                                        <p className={`font-bold ${isCorrect ? 'text-green-600' : 'text-red-600'}`}>
                                            {isCorrect ? 'Correct' : 'Incorrect'}
                                        </p>
                                    </div>
                                </li>
                            );
                        })}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default ReviewAssessment;
