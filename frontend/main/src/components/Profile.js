import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import AssessmentProgressChart from "./AssessmentProgressChart";

const Profile = () => {
    const navigate = useNavigate();
    const currentUser = useSelector((state) => state.user.currentUser?.user);
    console.log("user",currentUser);
    const [assessments, setAssessments] = useState([]);
    const [selectedAssessment, setSelectedAssessment] = useState(null);

    useEffect(() => {
        if (!currentUser) {
            navigate("/login-signup");
            return;
        }

        const fetchAssessments = async () => {
            try {
                const response = await fetch(`${process.env.REACT_APP_API_URL}/get_assessments/${currentUser.email}`);
                const data = await response.json();
                setAssessments(data);
            } catch (error) {
                console.error("Error fetching assessments:", error);
            }
        };

        fetchAssessments();
    }, [currentUser, navigate]);

    if (!currentUser) return null;

    const chartData = assessments.map((test, index) => ({
        name: `Test ${index + 1}`,
        score: ((test.questions.filter(q => q.selectedOption === q.answer).length / test.questions.length) * 100).toFixed(2),
    }));

    return (
        <div className="flex flex-col md:flex-row gap-6 max-w-6xl mx-auto p-6">
            {/* Left Sidebar */}
            <div className="md:w-1/3 bg-white shadow-lg rounded-lg p-6 border border-gray-200">
                <div className="flex flex-col items-center">
                    <img
                        src={currentUser.googlePhotoUrl || "https://via.placeholder.com/120"}
                        alt="Profile"
                        className="w-28 h-28 rounded-full border-4 border-gray-300"
                    />
                    <h2 className="text-xl font-bold mt-4">{currentUser?.name || "Guest"}</h2>
                    <p className="text-gray-600">{currentUser?.email}</p>
                </div>
            </div>

            {/* Right Section */}
            <div className="md:w-2/3 space-y-6">
                {/* Profile Completion */}
                {/* <div className="bg-white shadow-lg rounded-lg p-4 flex items-center justify-between border border-gray-200">
                    <h3 className="text-lg font-semibold">Complete your profile</h3>
                    <button className="bg-blue-500 text-white px-4 py-2 rounded-md">Complete Profile</button>
                </div> */}

                {/* Stats */}
                <div className="grid grid-cols-3 gap-4">
                    <div className="bg-white shadow-md p-4 rounded-lg border border-gray-200 text-center">
                        <h4 className="text-xl font-bold">{assessments.length}</h4>
                        <p className="text-gray-600">Assessments Taken</p>
                    </div>
                </div>

               

                {/* Assessment History */}
                <div className="bg-white shadow-lg rounded-lg p-6 border border-gray-200">
                    <h3 className="text-lg font-semibold mb-2">📜 Assessment History</h3>
                    <ul className="list-disc list-inside text-gray-600">
                        {assessments.length > 0 ? (
                            assessments.map((test, index) => (
                                <li key={index} className="mt-2 cursor-pointer text-blue-600 hover:underline" onClick={() => setSelectedAssessment(test)}>
                                    Test {index + 1} - Score: {chartData[index]?.score}%
                                </li>
                            ))
                        ) : (
                            <p>No assessments taken yet.</p>
                        )}
                    </ul>
                </div>
                 {/* Assessment Progress Chart */}
                 <div className="bg-white shadow-lg rounded-lg p-6 border border-gray-200">
                    <h3 className="text-lg font-semibold mb-4">📊 Assessment Progress</h3>
                    <AssessmentProgressChart data={chartData} />
                </div>
            </div>

            {selectedAssessment && (() => {
                let totalQuestions = selectedAssessment.questions.length;
                let correctCount = selectedAssessment.questions.reduce((count, questionObj) => {
                    return questionObj.selectedOption === questionObj.answer ? count + 1 : count;
                }, 0);
                let calculatedScore = ((correctCount / totalQuestions) * 100).toFixed(2);

                return (
                    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
                        <div className="bg-white p-6 rounded-lg shadow-lg max-w-lg w-full max-h-[80vh] overflow-y-auto">
                            <h3 className="text-2xl font-bold mb-4 text-gray-800">{selectedAssessment.title || "Assessment Details"}</h3>
                            <p className="text-lg font-semibold"><span className="text-purple-500">🏆 Score:</span> {calculatedScore}%</p>
                            <p className="text-gray-600"><strong>📅 Date:</strong> {selectedAssessment.date || "N/A"}</p>
                            <h4 className="text-lg font-semibold mt-4">🧐 Questions:</h4>

                            {selectedAssessment.questions && Array.isArray(selectedAssessment.questions) ? (
                                <ul className="list-none mt-2">
                                    {selectedAssessment.questions.map((questionObj, index) => {
                                        const { question, selectedOption, timeSpent, answer } = questionObj;
                                        const userAnswer = selectedOption !== null && selectedOption !== undefined 
                                            ? selectedOption 
                                            : "Not answered ❓";
                                        const correctAnswer = answer || "N/A";
                                        const isCorrect = selectedOption === answer;

                                        return (
                                            <li key={index} className="mb-4 p-4 border border-gray-300 rounded bg-gray-100">
                                                <h2 className="font-semibold">Q{index + 1}: {question}</h2>
                                                <p className="text-gray-600">⏳ Time Spent: {(timeSpent / 1000).toFixed(2)} seconds</p>
                                                <p className="text-gray-600">📝 Your Answer: {userAnswer}</p>
                                                <p className="text-gray-800">✅ Expected Answer: {correctAnswer}</p>
                                                <p className={isCorrect ? "text-green-600 font-bold" : "text-red-600 font-bold"}>
                                                    {isCorrect ? "✔ Correct" : "✖ Incorrect"}
                                                </p>
                                            </li>
                                        );
                                    })}
                                </ul>
                            ) : (
                                <p>No questions available.</p>
                            )}

                            <button className="mt-4 bg-red-500 text-white px-6 py-2 rounded hover:bg-red-600 transition" onClick={() => setSelectedAssessment(null)}>Close</button>
                        </div>
                    </div>
                );
            })()}
        </div>
    );
};

export default Profile;