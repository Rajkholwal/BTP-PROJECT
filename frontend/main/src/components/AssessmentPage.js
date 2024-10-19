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
  const { numQuestions, selectedTags, selectedLevel, loggedInName, loggedInEmail, loggedInType } = useLocation().state;
  const [selectedOptions, setSelectedOptions] = useState(Array(numQuestions).fill(null));
  const [feedback1, setFeedback1] = useState({});
  const [seconds, setSeconds] = useState(0);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [overallTimer, setOverallTimer] = useState(0);
  const [timeSpentPerQuestion, setTimeSpentPerQuestion] = useState(Array(parseInt(numQuestions)).fill(0));
  const [timerIntervals, setTimerIntervals] = useState([]);
  const sliderRef = useRef(null);
  const [isHovering1, setIsHovering1] = useState(false);
  let timerIntervalId;
  useEffect(() => {
    const fetchQuestionData = async () => {
      if (localStorage.getItem("questionsFetched")) {
        setQuestionsData(JSON.parse(localStorage.getItem("questionsFetched")));
        setLoading(false);
        return;
      }
      try {
        const payload = {
          tags: selectedTags,
          level: selectedLevel,
          numQuestions: numQuestions,
        };
        const response = await fetch(`${process.env.REACT_APP_API_URL}/startAssessment`, {
          method: 'POST',
          headers: {
            'content-type': 'application/json',
          },
          body: JSON.stringify(payload),
        });
        const data = await response.json();
        setQuestionsData(data.questions);
        for (let i = 0; i < data.questions.length; i++) {
          timeSpentPerQuestion[i] = 0;
        }
        setLoading(false);
        localStorage.setItem("questionsFetched", JSON.stringify(data.questions));

      } catch (error) {
        console.error(error);
        setLoading(false);
      }
    };
    fetchQuestionData();
  }, [numQuestions, selectedLevel, selectedTags]);

  useEffect(() => {
    const overallTimerInterval = setInterval(() => {
      setOverallTimer(prevOverallTimer => prevOverallTimer + 1000);
    }, 1000);

    return () => clearInterval(overallTimerInterval);
  }, []);

  useEffect(() => {
    const intervals = questionsData.map((_, index) => null);
    setTimerIntervals(intervals);
  }, [questionsData]);

  const formatTime = (milliseconds) => {
    const totalSeconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes > 0 ? `${minutes}m ` : ''}${seconds}s`;
  };

  const handleOptionSelect = (questionIndex, optionIndex) => {
    const newSelectedOptions = [...selectedOptions];
    newSelectedOptions[questionIndex] = optionIndex;
    setSelectedOptions(newSelectedOptions);
  };

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

  const handleSubmit = async () => {
    clearInterval(timerIntervalId);
    if (selectedOptions.includes(null)) {
      alert("Please answer all questions before submitting.");
      return;
    }
    if (Object.keys(feedback1).length !== questionsData.length) {
      alert("Please provide feedback for all questions before submitting.");
      return;
    }
    const completeFeedback = {
      selectedOptions: selectedOptions,
      correctOptions: {},
      feedback1: feedback1,
      name: loggedInName,
      email: loggedInEmail,
      type: loggedInType,
      questionBodies: questionsData,
      timeTaken: overallTimer,
      individualTimeTaken: timeSpentPerQuestion
    };

    questionsData.forEach((question, index) => {
      // if (question.answer[0][0] === 'A') {
      //   completeFeedback.correctOptions[index.toString()] = "0";
      // } else if (question.answer[0][0] === 'B') {
      //   completeFeedback.correctOptions[index.toString()] = "1";
      // } else if (question.answer[0][0] === 'C') {
      //   completeFeedback.correctOptions[index.toString()] = "2";
      // } else {
      //   completeFeedback.correctOptions[index.toString()] = "3";
      // }
      for(let i=0; i<question.options.length; i++){
        if (question.options[i] === question.answer)
          completeFeedback.correctOptions[index] = i;
      }
    });

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/submit_assessment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(completeFeedback),
      });
      const data = await response.json();
      const marksScored = data.marks_scored;
      const totalMarks = data.total_marks;
      const marks = [marksScored, totalMarks, formatTime(overallTimer)];
      localStorage.clear();
      navigate('/AssessmentDone', { state: { questions: questionsData, marks, loggedInName, loggedInEmail,selectedOptions,timeSpentPerQuestion } });
    } catch (error) {
      console.error(error);
    }
  };

  const handleMouseEnter1 = () => {
    setIsHovering1(true);
  };

  const handleMouseLeave1 = () => {
    setIsHovering1(false);
  };

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

  const handleDirectNavigation = (questionIndex) => {
    clearInterval(timerIntervals[currentQuestion]);
    setCurrentQuestion(questionIndex);
  };

  const [hoveredEmoji, setHoveredEmoji] = useState(null);

  const handleHover = (index) => {
    return () => setHoveredEmoji(meanings[index]);
  };

  const handleMouseOut = () => {
    setHoveredEmoji(null);
  };

  return (
    <div>
      {loading ? (
        <LoadingAssessment />
      ) : (
        <>
          <UpperNav name={loggedInName} email={loggedInEmail} />
          <div className="p-4">
            <div className="navigation-bar mb-4">
              <div className="mb-2 border border-green-200 rounded-lg shadow-md pt-2 pl-2 relative hover:shadow-lg transition duration-300" style={{ width: '20%', marginLeft: '10px' }}>
                <div className="mb-4 text-gray-800">Overall Timer: {formatTime(overallTimer)}</div>
              </div>
              {questionsData.map((_, index) => (
                <button
                  key={index}
                  className={`nav-button ${index === currentQuestion ? 'active' : ''} ${selectedOptions[index] !== null ? 'answered' : 'unanswered'}`}
                  onClick={() => handleDirectNavigation(index)}
                  style={{
                    backgroundColor: index === currentQuestion ? '#4CAF50' : selectedOptions[index] !== null ? '#2196F3' : '#ddd',
                    color: index === currentQuestion ? 'white' : selectedOptions[index] !== null ? 'white' : 'black',
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

            {questionsData.map((questionObj, questionIndex) => (
              <div key={questionIndex} className={`bg-gray-200 p-4 rounded shadow ${questionIndex === currentQuestion ? 'block' : 'hidden'}`}>
                {/* Render question first */}
                <h2 className="text-2xl font-bold mb-4">Q{questionIndex + 1}: {questionObj.question.split('\n').map((textChunk, index) => (<span key={index}>{textChunk}<br /></span>))}</h2>

                {/* Render image below the question */}
                {questionObj.images?.map((image, imgIndex) => (
                  <SvgDisplay key={imgIndex} svgContent={image} />
                ))}

                {/* Render options below the image */}
                <ul className="list-none">
                  {questionObj.options.map((option, optionIndex) => (
                    <div key={optionIndex} className="flex items-center mb-2 cursor-pointer" onClick={() => handleOptionSelect(questionIndex, optionIndex)}>
                      <input
                        type="radio"
                        name={`question-${questionIndex}`}
                        checked={selectedOptions[questionIndex] === optionIndex}
                        className="mr-2"
                      />
                      <div className={`list-disc ml-4 ${selectedOptions[questionIndex] === optionIndex ? 'text-blue-500 font-bold' : ''}`}>
                        {option}
                      </div>
                    </div>
                  ))}
                </ul>

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
                <div className='flex'>
                  <div className="mr-2 border border-red-200 rounded-lg shadow-md p-4 relative hover:shadow-lg transition duration-300" style={{ width: '20%' }}>
                    <div className="mb-4 text-black-800 font-bold">
                      Time Spent on this question: {formatTime(timeSpentPerQuestion[questionIndex])}
                    </div>
                  </div>
                  <div className="border border-red-200 rounded-lg shadow-md p-4 relative hover:shadow-lg transition duration-300" style={{ width: '20%' }} onMouseEnter={handleMouseEnter1} onMouseLeave={handleMouseLeave1}>
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
