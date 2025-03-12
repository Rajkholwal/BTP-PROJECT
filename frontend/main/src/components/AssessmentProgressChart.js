import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const AssessmentProgressChart = ({ data }) => {
    if (!data.length) return <p className="text-gray-600">No assessment data available.</p>;

    return (
        <div className="bg-gray-100 p-6 rounded-lg shadow-md mt-6">
            <h3 className="text-xl font-semibold mb-4 text-gray-700">📊 Progress Over Time</h3>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Line type="monotone" dataKey="score" stroke="#4f46e5" strokeWidth={3} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default AssessmentProgressChart;
