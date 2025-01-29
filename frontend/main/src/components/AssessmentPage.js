import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import LoadingAssessment from './LoadingAssessment';
import UpperNav from './UpperNav';
import SvgDisplay from './SvgDisplay';

const emojis = ['😁', '😖', '⏲️', '😢', '❓'];
const meanings = ['Easy', 'Difficult', 'Time consuming', 'Out of Scope', 'Ambiguous'];

const AssessmentPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [questionsData, setQuestionsData] = useState([]);
  
  // Grab data from the route/state
  const {
    numQuestions,
    selectedTags,
    selectedLevel,
    loggedInName,
    loggedInEmail,
    loggedInType,
  } = useLocation().state;

  const [selectedOptions, setSelectedOptions] = useState(Array(numQuestions).fill(null));
  const [feedback1, setFeedback1] = useState({});
  const [currentQuestion, setCurrentQuestion] = useState(0);
  
  const [overallTimer, setOverallTimer] = useState(0);
  const [timeSpentPerQuestion, setTimeSpentPerQuestion] = useState(
    Array(parseInt(numQuestions)).fill(0)
  );
  const [timerIntervals, setTimerIntervals] = useState([]);
  
  const [isHovering1, setIsHovering1] = useState(false);
  const [hoveredEmoji, setHoveredEmoji] = useState(null);

  let timerIntervalId;

  // Fetch question data on mount
  useEffect(() => {
    const fetchQuestionData = async () => {
      if (localStorage.getItem('questionsFetched')) {
        setQuestionsData(JSON.parse(localStorage.getItem('questionsFetched')));
        setLoading(false);
        return;
      }
      try {
        const payload = {
          tags: selectedTags,
          level: selectedLevel,
          numQuestions: numQuestions,
        };
        // Example: fetch from your /startAssessment route
        // Adjust according to your actual server endpoint
        const response = await fetch(`${process.env.REACT_APP_API_URL}/startAssessment`, {
          method: 'POST',
          headers: {
            'content-type': 'application/json',
          },
          body: JSON.stringify(payload),
        });
        const data = await response.json();
        setQuestionsData(data.questions);

        // Initialize timeSpent array
        for (let i = 0; i < data.questions.length; i++) {
          timeSpentPerQuestion[i] = 0;
        }
        setLoading(false);
        localStorage.setItem('questionsFetched', JSON.stringify(data.questions));
      } catch (error) {
        console.error(error);
        setLoading(false);
      }
    };
    fetchQuestionData();
  }, [numQuestions, selectedLevel, selectedTags, timeSpentPerQuestion]);

  // Overall Timer
  useEffect(() => {
    const overallTimerInterval = setInterval(() => {
      setOverallTimer(prevOverallTimer => prevOverallTimer + 1000);
    }, 1000);
    return () => clearInterval(overallTimerInterval);
  }, []);

  // Create placeholders for timer intervals
  useEffect(() => {
    const intervals = questionsData.map(() => null);
    setTimerIntervals(intervals);
  }, [questionsData]);

  // Format milliseconds into Mins + Secs
  const formatTime = (milliseconds) => {
    const totalSeconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes > 0 ? `${minutes}m ` : ''}${seconds}s`;
  };

  // Handle radio option selection
  const handleOptionSelect = (questionIndex, optionIndex) => {
    const newSelectedOptions = [...selectedOptions];
    newSelectedOptions[questionIndex] = optionIndex;
    setSelectedOptions(newSelectedOptions);
  };

  // Feedback (emojis)
  const handleFeedbackChange1 = (questionIndex, feedbackType) => {
    setFeedback1(prevFeedback => ({
      ...prevFeedback,
      [questionIndex]: feedbackType,
    }));
  };

  const handlePrev = () => {
    setCurrentQuestion(prevQuestion => Math.max(0, prevQuestion - 1));
  };

  const handleNext = () => {
    setCurrentQuestion(prevQuestion => Math.min(questionsData.length - 1, prevQuestion + 1));
  };

  // **No backend submission** - Calculate marks on the frontend
  const handleSubmit = () => {
    clearInterval(timerIntervalId);

    // Ensure each question is answered
    if (selectedOptions.includes(null)) {
      alert('Please answer all questions before submitting.');
      return;
    }

    // Ensure each question has feedback
    if (Object.keys(feedback1).length !== questionsData.length) {
      alert('Please provide feedback for all questions before submitting.');
      return;
    }

    // Calculate total marks vs. marks scored
    let totalMarks = questionsData.length;
    let marksScored = 0;

    // For each question, figure out the correct option index
    questionsData.forEach((question, index) => {
      const correctIndex = question.options.indexOf(question.answer);
      if (correctIndex === selectedOptions[index]) {
        marksScored++;
      }
    });

    // Prepare data to show on results page
    const completeTime = formatTime(overallTimer);
    const marksInfo = [marksScored, totalMarks, completeTime];

    // Clear local storage if needed
    localStorage.clear();

    // Navigate to next page (AssessmentDone), passing results
    navigate('/AssessmentDone', {
      state: {
        questions: questionsData,
        marks: marksInfo,            // [marksScored, totalMarks, timeString]
        loggedInName,
        loggedInEmail,
        selectedOptions,
        timeSpentPerQuestion,
      },
    });
  };

  // Hover behavior for emoji feedback
  const handleMouseEnter1 = () => {
    setIsHovering1(true);
  };
  const handleMouseLeave1 = () => {
    setIsHovering1(false);
  };
  const handleHover = (index) => () => {
    setHoveredEmoji(meanings[index]);
  };
  const handleMouseOut = () => {
    setHoveredEmoji(null);
  };

  // Track how much time each question gets
  useEffect(() => {
    timerIntervalId = setInterval(() => {
      setTimeSpentPerQuestion(prevTimeSpent => {
        const updatedTimeSpent = [...prevTimeSpent];
        updatedTimeSpent[currentQuestion] += 1000;
        return updatedTimeSpent;
      });
    }, 1000);

    return () => {
      clearInterval(timerIntervalId);
    };
  }, [currentQuestion]);

  // Jump to a question directly
  const handleDirectNavigation = (questionIndex) => {
    clearInterval(timerIntervals[currentQuestion]);
    setCurrentQuestion(questionIndex);
  };

  return (
    <div>
      {loading ? (
        <LoadingAssessment />
      ) : (
        <>
          <UpperNav name={loggedInName} email={loggedInEmail} />
          <div className="p-4">
            {/* Top navigation for questions + overall timer */}
            <div className="navigation-bar mb-4">
              <div
                className="mb-2 border border-green-200 rounded-lg shadow-md pt-2 pl-2 relative hover:shadow-lg transition duration-300"
                style={{ width: '20%', marginLeft: '10px' }}
              >
                <div className="mb-4 text-gray-800">
                  Overall Timer: {formatTime(overallTimer)}
                </div>
              </div>

              {/* Buttons for each question */}
              {questionsData.map((_, index) => (
                <button
                  key={index}
                  className={`nav-button ${index === currentQuestion ? 'active' : ''} ${
                    selectedOptions[index] !== null ? 'answered' : 'unanswered'
                  }`}
                  onClick={() => handleDirectNavigation(index)}
                  style={{
                    backgroundColor:
                      index === currentQuestion
                        ? '#4CAF50'
                        : selectedOptions[index] !== null
                        ? '#2196F3'
                        : '#ddd',
                    color:
                      index === currentQuestion || selectedOptions[index] !== null
                        ? 'white'
                        : 'black',
                    border: 'none',
                    borderRadius: '5px',
                    padding: '10px 20px',
                    margin: '5px',
                    cursor: 'pointer',
                    minWidth: '50px',
                    maxWidth: '150px',
                    transition: 'background-color 0.3s',
                  }}
                >
                  {`Q ${index + 1}`}
                  {selectedOptions[index] != null ? (
                    <span style={{ marginLeft: '5px' }}>✔️</span>
                  ) : (
                    <span style={{ marginLeft: '5px', color: '#FF5733' }}>❌</span>
                  )}
                </button>
              ))}
            </div>

            {/* Render each question (only show current question) */}
            {questionsData.map((questionObj, questionIndex) => (
              <div
                key={questionIndex}
                className={`bg-gray-200 p-4 rounded shadow ${
                  questionIndex === currentQuestion ? 'block' : 'hidden'
                }`}
              >
                {/* Question text */}
                <h2 className="text-2xl font-bold mb-4">
                  Q{questionIndex + 1}:{' '}
                  {questionObj.question.split('\n').map((textChunk, index) => (
                    <span key={index}>
                      {textChunk}
                      <br />
                    </span>
                  ))}
                </h2>

                {/* Possible images under the question */}
                {questionObj.images?.map((image, imgIndex) => (
                  <SvgDisplay key={imgIndex} svgContent={image} />
                ))}

                {/* Options (radio) */}
                <ul className="list-none">
                  {questionObj.options.map((option, optionIndex) => (
                    <div
                      key={optionIndex}
                      className="flex items-center mb-2 cursor-pointer"
                      onClick={() => handleOptionSelect(questionIndex, optionIndex)}
                    >
                      <input
                        type="radio"
                        name={`question-${questionIndex}`}
                        checked={selectedOptions[questionIndex] === optionIndex}
                        className="mr-2"
                      />
                      <div
                        className={`list-disc ml-4 ${
                          selectedOptions[questionIndex] === optionIndex
                            ? 'text-blue-500 font-bold'
                            : ''
                        }`}
                      >
                        {option}
                      </div>
                    </div>
                  ))}
                </ul>

                {/* Prev / Next buttons */}
                <div className="mb-5 ml-5 mr-5 mt-4 flex justify-between">
                  <button
                    className="bg-blue-500 text-white px-4 py-2 rounded"
                    onClick={handlePrev}
                    disabled={currentQuestion === 0}
                  >
                    Previous
                  </button>
                  <button
                    className="bg-blue-500 text-white px-4 py-2 rounded"
                    onClick={handleNext}
                    disabled={currentQuestion === questionsData.length - 1}
                  >
                    Next
                  </button>
                </div>

                {/* Time spent on this question + Rate This? */}
                <div className="flex">
                  <div
                    className="mr-2 border border-red-200 rounded-lg shadow-md p-4 relative hover:shadow-lg transition duration-300"
                    style={{ width: '20%' }}
                  >
                    <div className="mb-4 text-black-800 font-bold">
                      Time Spent on this question:{' '}
                      {formatTime(timeSpentPerQuestion[questionIndex])}
                    </div>
                  </div>
                  <div
                    className="border border-red-200 rounded-lg shadow-md p-4 relative hover:shadow-lg transition duration-300"
                    style={{ width: '20%' }}
                    onMouseEnter={handleMouseEnter1}
                    onMouseLeave={handleMouseLeave1}
                  >
                    <div className="mb-4 text-blue-800">
                      Rate this?
                      {isHovering1 && (
                        <div className="display-flex absolute mb-5">
                          {emojis.map((emoji, index) => (
                            <span
                              key={index}
                              onMouseOver={handleHover(index)}
                              onMouseOut={handleMouseOut}
                              onClick={() => handleFeedbackChange1(questionIndex, emoji)}
                              className="cursor-pointer text-xl"
                            >
                              {emoji}
                            </span>
                          ))}
                          {hoveredEmoji && <div className="tooltip">{hoveredEmoji}</div>}
                        </div>
                      )}
                    </div>
                    {feedback1[questionIndex] && (
                      <div className="pt-10 text-lg text-black-700 font-medium">
                        You selected: {feedback1[questionIndex]}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}

            {/* Final Submit button */}
            <div className="mt-6 flex justify-center">
              <button
                onClick={handleSubmit}
                className="bg-green-500 text-white px-6 py-2 rounded hover:bg-green-700 transition duration-300"
              >
                Submit
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default AssessmentPage;
