import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const QuizForm = (props) => {
  const [selectedTags, setSelectedTags] = useState([]);
  const [selectedLevel, setSelectedLevel] = useState(null);
  const [numQuestions, setNumQuestions] = useState('');
  const {loggedInName,loggedInEmail,loggedInType} = props

  const navigate = useNavigate()


  const handleTagClick = (tag) => {
    if (selectedTags.includes(tag)) {
      setSelectedTags(selectedTags.filter((selectedTag) => selectedTag !== tag));
    } else {
      setSelectedTags([...selectedTags, tag]);
    }
  };

  const handleLevelClick = (level) => {
    setSelectedLevel(level);
  };

  const handleInputChange = (event) => {
    let inputValue = event.target.value;
    if(inputValue > 50){
      inputValue = 50;
    }
    else if(inputValue<0)
    {
      inputValue = 1;
    }
    setNumQuestions(inputValue);
  };

  const handleGeneratePdf = async (event) => {
    console.log(selectedTags)
    console.log(selectedLevel)
    console.log(numQuestions)
    event.preventDefault();

    // Create payload to send to the server
    const payload = {
      tags: selectedTags,
      level: selectedLevel,
      numQuestions: numQuestions,
    };

    try {
      // Send POST request to the Flask server
      const response = await fetch(`${process.env.REACT_APP_API_URL}/submit_quiz`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      // Handle the response as needed
      if (response.ok) {
        alert('Quiz submitted successfully!');
      } else {
        console.error('Failed to submit quiz.');
        console.log(response.statusText)
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleStartAssessment = async (event) => {
    // Create payload to send to the server
    console.log(loggedInName)
    try {
      navigate('/AssessmentPage', { state: { numQuestions, selectedTags, selectedLevel, loggedInName, loggedInEmail, loggedInType } })
    } catch (error) {
      console.log(error)
    }

  }

  const tags = [
    'Number-System',
    'Boolean-algebra',
    'Logic-Gates',
    'Flip-flops',
    'SequenceDetector',
    'Truth-Tables',
    'State-Machine',
    'State-Table',
  ];
  const levels = ['Easy', 'Medium'];

  return (
    <div className="px-6 lg:px-8">
      <div className="mx-auto mt-10 max-w-6xl">
        <div className="rounded-3xl border border-gray-200 bg-white p-8 shadow">
          <div className="text-center">
            <h1 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-5xl">
              Digital Logic Design Quiz Generator
            </h1>
            <p className="mt-4 text-base leading-7 text-slate-600 sm:text-lg">
              Choose modules, difficulty, and number of questions for your assessment.
            </p>
          </div>

          <div className="mt-10 grid gap-8 lg:grid-cols-3">
            <div className="lg:col-span-2">
              <div className="space-y-6">
                {/* Tag Selector */}
                <div>
                  <h3 className="text-lg font-semibold text-slate-900 mb-3">Select Modules</h3>
                  <div className="flex flex-wrap gap-2">
                    {tags.map((tag) => (
                      <span
                        key={tag}
                        className={`inline-flex items-center rounded-full px-3 py-1 text-sm font-semibold cursor-pointer border transition ${
                          selectedTags.includes(tag)
                            ? 'bg-emerald-600 text-white border-emerald-600'
                            : 'bg-white text-slate-700 border-gray-300 hover:bg-gray-50'
                        }`}
                        onClick={() => handleTagClick(tag)}
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Level Selector */}
                <div>
                  <h3 className="text-lg font-semibold text-slate-900 mb-3">Select Difficulty</h3>
                  <div className="flex flex-wrap gap-2">
                    {levels.map((level) => (
                      <span
                        key={level}
                        className={`inline-flex items-center rounded-full px-3 py-1 text-sm font-semibold cursor-pointer border transition ${
                          selectedLevel === level
                            ? 'bg-emerald-600 text-white border-emerald-600'
                            : 'bg-white text-slate-700 border-gray-300 hover:bg-gray-50'
                        }`}
                        onClick={() => handleLevelClick(level)}
                      >
                        {level}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Question Input */}
                <div>
                  <h3 className="text-lg font-semibold text-slate-900">Number of Questions</h3>
                  
                  <form className="mt-3 flex items-center gap-3">
                    <label htmlFor="numQuestionsInput" className="text-slate-700">
                      Questions:
                    </label>
                    <input
                      type="number"
                      id="numQuestionsInput"
                      className="w-32 rounded-md border border-gray-300 bg-white px-3 py-2 text-slate-900 outline-none focus:border-emerald-600 focus:ring-2 focus:ring-emerald-600/20"
                      value={numQuestions}
                      onChange={handleInputChange}
                    />
                  </form>
                  <div className="mt-2 text-sm text-slate-500">(maximum 50 questions allowed)</div>
                </div>
              </div>

              {/* Submit Button */}
              <div className="mt-8 flex flex-wrap gap-3">
                <button
                  onClick={handleGeneratePdf}
                  className="rounded-md bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-slate-800"
                >
                  Generate PDF
                </button>
                <button
                  onClick={handleStartAssessment}
                  className="rounded-md bg-emerald-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-emerald-500"
                >
                  Start Assessment
                </button>
              </div>
            </div>

            <aside className="rounded-2xl border border-gray-200 bg-gray-50 p-5">
              <div className="text-sm font-semibold text-slate-900">Tips</div>
              <ul className="mt-3 space-y-2 text-sm text-slate-600">
                <li>- Select multiple modules to mix question types.</li>
                <li>- Pick difficulty first for better distribution.</li>
                <li>- Start with 10–20 questions for fastest results.</li>
              </ul>
            </aside>
          </div>
        </div>
      </div>
    </div>
  );
};


export default QuizForm;
