import React, { useState } from 'react';

const LevelSelector = () => {
  const [selectedLevel, setSelectedLevel] = useState(null);

  const handleLevelClick = (level) => {
    setSelectedLevel(level);
  };

  const levels = ['L1', 'L2', 'L3'];

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Select Level</h2>
      <div className="space-x-2">
        {levels.map((level) => (
          <span
            key={level}
            className={`inline-block px-3 py-1 text-sm font-semibold rounded-full cursor-pointer ${
              selectedLevel === level ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'
            }`}
            onClick={() => handleLevelClick(level)}
          >
            {level}
          </span>
        ))}
      </div>
      {/* <div className="mt-4">
        <p className="text-gray-700">Selected Level: {selectedLevel || 'None'}</p>
      </div> */}
    </div>
  );
};

export default LevelSelector;
