import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import UpperNav from './UpperNav';

const QuizForm = (props) => {
  const [selectedTags, setSelectedTags] = useState([]);
  const [selectedLevel, setSelectedLevel] = useState(null);
  const [numQuestions, setNumQuestions] = useState('');
  const [generated, setgenerated] = useState(0)
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
        setgenerated(0)
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
    const payload = {
      tags: selectedTags,
      level: selectedLevel,
      numQuestions: numQuestions,
    };
    try {
      navigate('/AssessmentPage', { state: { numQuestions, selectedTags, selectedLevel, loggedInName, loggedInEmail, loggedInType } })
    } catch (error) {
      console.log(error)
    }

  }

  const tags = ['Number-System', 'Boolean-algebra', 'Logic-Gates', 'SequenceDetector', 'Truth-Tables', 'State-Machine','State-Table'];
  const levels = ['Easy', 'Medium'];

  return (
    <div>
      <div class="relative isolate px-6 lg:px-8">
        <div class="mt-5">
          <div class="hidden sm:mb-8 sm:flex sm:justify-center">
            <div class="relative rounded-full px-3 text-sm leading-6 text-gray-600 ring-1 ring-gray-900/10 hover:ring-gray-900/20">
              More about out plan:   <a href="#" class="font-semibold text-indigo-600"><span class="absolute inset-0" aria-hidden="true"></span>Read more <span aria-hidden="true">&rarr;</span></a>
            </div>
          </div>
          <div class="text-center">
            <h1 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">Digital Logic Design Quiz generator</h1>
            <p class="mt-6 text-lg leading-8 text-gray-600">Fill details about the tags you want to include along with the level and number of questions you want to generate in your quiz.</p>
            <div className="p-10">
              <h2 className="text-xl font-bold mb-4">Quiz Configuration</h2>
              <div className="space-y-4">
                {/* Tag Selector */}
                <div>
                  <h3 className="text-lg font-semibold mb-2">Select Tags</h3>
                  <div className="space-x-2">
                    {tags.map((tag) => (
                      <span
                        key={tag}
                        className={`inline-block px-3 py-1 text-sm font-semibold rounded-full cursor-pointer ${selectedTags.includes(tag) ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'
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
                  <h3 className="text-lg font-semibold mb-2">Select Level</h3>
                  <div className="space-x-2">
                    {levels.map((level) => (
                      <span
                        key={level}
                        className={`inline-block px-3 py-1 text-sm font-semibold rounded-full cursor-pointer ${selectedLevel === level ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'
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
                  <h3 className="text-lg font-semibold">Enter Number of Questions</h3>
                  
                  <form className="display-flex mb-2">
                    <label htmlFor="numQuestionsInput" className="text-gray-700 pr-2 ">
                      Questions:
                    </label>
                    <input
                      type="number"
                      id="numQuestionsInput"
                      className=" p-2 border rounded-md"
                      value={numQuestions}
                      onChange={handleInputChange}
                    />
                  </form>
                  <h4 className="mb-2">(maximum 50 questions are allowed per assessment)</h4>
                </div>
              </div>

              {/* Submit Button */}
              <div className="mt-4">
                <button
                  onClick={handleGeneratePdf}
                  className="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                >
                  Generate PDF
                </button>
                <button
                  onClick={handleStartAssessment}
                  className="ml-8 rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                >
                  Start Assessment
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="absolute inset-x-0 top-[calc(100%-13rem)] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[calc(100%-30rem)]" aria-hidden="true">
          <div class="relative left-[calc(50%+3rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%+36rem)] sm:w-[72.1875rem]"></div>
        </div>
      </div>
    </div>
  );
};


export default QuizForm;
