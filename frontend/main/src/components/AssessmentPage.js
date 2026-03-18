import React, { useMemo, useRef, useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import LoadingAssessment from './LoadingAssessment';
import SvgDisplay from './SvgDisplay';

const AssessmentPage = () => {
  const navigate = useNavigate();
  // const currentUser = useSelector((state) => state.user.currentUser.user);
  
  const [loading, setLoading] = useState(true);
  const [questionsData, setQuestionsData] = useState([]);
  const { numQuestions, selectedTags, selectedLevel, loggedInName, loggedInEmail, loggedInType } = useLocation().state;
  const [selectedOptions, setSelectedOptions] = useState(Array(numQuestions).fill(null));
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [overallTimer, setOverallTimer] = useState(0);
  const [timeSpentPerQuestion, setTimeSpentPerQuestion] = useState(Array(parseInt(numQuestions)).fill(0));
  const [timerIntervals, setTimerIntervals] = useState([]);
  const [visited, setVisited] = useState(() => Array(parseInt(numQuestions)).fill(false));
  const [markedForReview, setMarkedForReview] = useState(() => Array(parseInt(numQuestions)).fill(false));
  const [showSubmitConfirm, setShowSubmitConfirm] = useState(false);
  const [submitConfirmed, setSubmitConfirmed] = useState(false);
  const timerIntervalIdRef = useRef(null);
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
        const response = await fetch(`${process.env.REACT_APP_API_URL}/startAssessment`, {
          method: 'POST',
          headers: {
            'content-type': 'application/json',
          },
          body: JSON.stringify(payload),
        });
        const data = await response.json();
        setQuestionsData(data.questions);
        setVisited(Array(data.questions.length).fill(false));
        setMarkedForReview(Array(data.questions.length).fill(false));
        setLoading(false);
        localStorage.setItem("questionsFetched", JSON.stringify(data.questions));

      } catch (error) {
        console.error(error);
        setLoading(false);
      }
    };
    fetchQuestionData();
  }, [numQuestions, selectedLevel, selectedTags, timeSpentPerQuestion]);

  useEffect(() => {
    const overallTimerInterval = setInterval(() => {
      setOverallTimer(prevOverallTimer => prevOverallTimer + 1000);
    }, 1000);

    return () => clearInterval(overallTimerInterval);
  }, []);

  useEffect(() => {
    const intervals = questionsData.map(() => null);
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

  const handleToggleMarkForReview = () => {
    setMarkedForReview(prev => {
      const next = [...prev];
      next[currentQuestion] = !next[currentQuestion];
      return next;
    });
  };

  const handlePrev = () => {
    setCurrentQuestion(prevQuestion => Math.max(0, prevQuestion - 1));
  };

  const handleNext = () => {
    setCurrentQuestion(prevQuestion => Math.min(questionsData.length - 1, prevQuestion + 1));
  };

  useEffect(() => {
    setVisited(prev => {
      if (!questionsData.length) return prev;
      const next = [...prev];
      next[currentQuestion] = true;
      return next;
    });
  }, [currentQuestion, questionsData.length]);

  const statusCounts = useMemo(() => {
    const total = questionsData.length;
    let notVisited = 0;
    let notAnswered = 0;
    let answered = 0;
    let marked = 0;

    for (let i = 0; i < total; i++) {
      const isVisited = !!visited[i];
      const isAnswered = selectedOptions[i] !== null && selectedOptions[i] !== undefined;
      const isMarked = !!markedForReview[i];

      if (!isVisited) notVisited++;
      if (isMarked) marked++;

      if (isVisited && !isAnswered) notAnswered++;
      if (isAnswered) answered++;
    }

    return { total, notVisited, notAnswered, answered, marked };
  }, [markedForReview, questionsData.length, selectedOptions, visited]);

  const handleSubmit = async () => {
    if (timerIntervalIdRef.current) clearInterval(timerIntervalIdRef.current);

    const completeFeedback = {
        selectedOptions: selectedOptions,
        correctOptions: {},  // To be filled
        name: loggedInName,
        email: loggedInEmail,
        type: loggedInType,
        questionBodies: questionsData,
        timeTaken: overallTimer,
        individualTimeTaken: timeSpentPerQuestion
    };

    let totalMarks = questionsData.length;
    let marksScored = 0;

    // Compute correct options and score
    questionsData.forEach((question, index) => {
        const correctIndex = question.options.indexOf(question.answer);
        completeFeedback.correctOptions[index] = correctIndex; // Store correct option index

        if (selectedOptions[index] !== null && selectedOptions[index] === correctIndex) {
            marksScored++;
        }
    });

    // try {
    //     await fetch(`${process.env.REACT_APP_API_URL}/submit_user_assessment`, {
    //         method: 'POST',
    //         headers: { 'Content-Type': 'application/json' },
    //         body: JSON.stringify({
    //             email: currentUser?.email,  // Ensure `currentUser` exists
    //             assessments: completeFeedback
    //         }),
    //     });

    // } catch (error) {
    //     console.error(error);
    // }

    // Prepare results data
    const completeTime = formatTime(overallTimer);
    const marksInfo = [marksScored, totalMarks, completeTime];

    // Clear local storage
    localStorage.clear();

    // Navigate to results page
    navigate('/AssessmentDone', {
        state: {
            questions: questionsData,
            marks: marksInfo,
            loggedInName,
            loggedInEmail,
            selectedOptions,
            timeSpentPerQuestion,
            markedForReview,
            visited,
        },
    });
};



  useEffect(() => {
    timerIntervalIdRef.current = setInterval(() => {
      setTimeSpentPerQuestion(prevTimeSpent => {
        const updatedTimeSpent = [...prevTimeSpent];
        updatedTimeSpent[currentQuestion] += 1000;
        return updatedTimeSpent;
      });
    }, 1000);

    return () => {
      if (timerIntervalIdRef.current) clearInterval(timerIntervalIdRef.current);
    };
  }, [currentQuestion]);

  const handleDirectNavigation = (questionIndex) => {
    clearInterval(timerIntervals[currentQuestion]);
    setCurrentQuestion(questionIndex);
  };

  const getPaletteStyle = (index) => {
    const isVisited = !!visited[index];
    const isAnswered = selectedOptions[index] !== null && selectedOptions[index] !== undefined;
    const isMarked = !!markedForReview[index];

    // NTA-style mapping:
    // - Not visited: Grey
    // - Visited but not answered: Red
    // - Answered: Green
    // - Marked for review (not answered): Yellow
    // - Marked for review (answered): Yellow + border
    if (!isVisited) return { bg: 'bg-gray-300', text: 'text-black', ring: '' };
    if (isMarked && isAnswered) return { bg: 'bg-yellow-300', text: 'text-black', ring: 'ring-2 ring-green-600' };
    if (isMarked) return { bg: 'bg-yellow-300', text: 'text-black', ring: '' };
    if (isAnswered) return { bg: 'bg-green-600', text: 'text-white', ring: '' };
    return { bg: 'bg-red-600', text: 'text-white', ring: '' };
  };

  const jumpToFirst = (predicate) => {
    const idx = questionsData.findIndex((_, i) => predicate(i));
    if (idx >= 0) {
      setShowSubmitConfirm(false);
      setSubmitConfirmed(false);
      handleDirectNavigation(idx);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 text-slate-900">
      {loading ? (
        <LoadingAssessment />
      ) : (
        <>
          {/* <UpperNav name={loggedInName} email={loggedInEmail} /> */}
          <div className="mx-auto grid max-w-7xl grid-cols-1 gap-4 p-4 lg:grid-cols-12">
            {/* Main question area */}
            <div className="lg:col-span-8">
              {questionsData.map((questionObj, questionIndex) => (
                <div key={questionIndex} className={`rounded-lg bg-gray-200 p-4 shadow text-slate-900 ${questionIndex === currentQuestion ? 'block' : 'hidden'}`}>
                {/* Render question first */}
                <h2 className="text-2xl font-bold mb-4 text-black">
                  Q{questionIndex + 1}:{' '}
                  {questionObj.question.split('\n').map((textChunk, index) => (
                    <span key={index}>
                      {textChunk}
                      <br />
                    </span>
                  ))}
                </h2>

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
                      <div className={`list-disc ml-4 text-black ${selectedOptions[questionIndex] === optionIndex ? 'text-blue-600 font-bold' : ''}`}>
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
                    className={`${markedForReview[currentQuestion] ? 'bg-yellow-500 hover:bg-yellow-600' : 'bg-yellow-400 hover:bg-yellow-500'} text-black px-4 py-2 rounded`}
                    onClick={handleToggleMarkForReview}
                  >
                    {markedForReview[currentQuestion] ? 'Unmark Review' : 'Mark for Review'}
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
                </div>
                </div>
              ))}
            </div>

            {/* Sidebar palette */}
            <aside className="lg:col-span-4">
              <div className="sticky top-4 rounded-lg border border-gray-200 bg-white p-4 shadow">
                <div className="flex items-center justify-between">
                  <div className="text-sm font-semibold text-slate-900">Question Palette</div>
                  <div className="text-sm text-slate-700">Time: {formatTime(overallTimer)}</div>
                </div>

                <div className="mt-3 grid grid-cols-6 gap-2">
                  {questionsData.map((_, index) => {
                    const st = getPaletteStyle(index);
                    return (
                      <button
                        key={index}
                        type="button"
                        onClick={() => handleDirectNavigation(index)}
                        className={`h-9 rounded ${st.bg} ${st.text} ${st.ring} text-sm font-semibold`}
                        title={`Q${index + 1}`}
                      >
                        {index + 1}
                      </button>
                    );
                  })}
                </div>

                <div className="mt-4 space-y-2 text-sm text-slate-800">
                  <div className="font-semibold text-slate-900">Legend</div>
                  <div className="flex items-center gap-2"><span className="inline-block h-3 w-3 rounded bg-gray-300" /> Not visited</div>
                  <div className="flex items-center gap-2"><span className="inline-block h-3 w-3 rounded bg-red-600" /> Visited & not answered</div>
                  <div className="flex items-center gap-2"><span className="inline-block h-3 w-3 rounded bg-green-600" /> Answered</div>
                  <div className="flex items-center gap-2"><span className="inline-block h-3 w-3 rounded bg-yellow-300" /> Marked for review</div>
                  <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-slate-700">
                    <div>Not visited: <span className="font-semibold">{statusCounts.notVisited}</span></div>
                    <div>Not answered: <span className="font-semibold">{statusCounts.notAnswered}</span></div>
                    <div>Answered: <span className="font-semibold">{statusCounts.answered}</span></div>
                    <div>Marked: <span className="font-semibold">{statusCounts.marked}</span></div>
                  </div>
                </div>

                <button
                  onClick={() => setShowSubmitConfirm(true)}
                  className="mt-4 w-full rounded bg-green-600 px-4 py-2 text-sm font-semibold text-white hover:bg-green-700"
                >
                  Submit
                </button>
              </div>
            </aside>
          </div>

          {/* Submit confirm modal */}
          {showSubmitConfirm && (
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
              <div className="w-full max-w-md rounded-lg bg-white p-5 shadow-xl">
                <div className="text-lg font-semibold text-slate-900">Ready to submit?</div>
                <div className="mt-2 text-sm text-slate-700">
                  Please review your attempt summary:
                </div>
                <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
                  <button
                    type="button"
                    onClick={() => jumpToFirst(() => true)}
                    className="rounded border border-gray-200 p-3 text-left hover:bg-gray-50"
                    title="Jump to first question"
                  >
                    Total: <span className="font-semibold">{statusCounts.total}</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => jumpToFirst((i) => (selectedOptions[i] ?? null) !== null)}
                    className="rounded border border-gray-200 p-3 text-left hover:bg-gray-50"
                    title="Jump to first answered question"
                  >
                    Answered: <span className="font-semibold">{statusCounts.answered}</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => jumpToFirst((i) => !!visited[i] && (selectedOptions[i] ?? null) === null)}
                    className="rounded border border-gray-200 p-3 text-left hover:bg-gray-50"
                    title="Jump to first visited but not answered"
                  >
                    Not answered: <span className="font-semibold">{statusCounts.notAnswered}</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => jumpToFirst((i) => !visited[i])}
                    className="rounded border border-gray-200 p-3 text-left hover:bg-gray-50"
                    title="Jump to first not visited"
                  >
                    Not visited: <span className="font-semibold">{statusCounts.notVisited}</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => jumpToFirst((i) => !!markedForReview[i])}
                    className="rounded border border-gray-200 p-3 text-left hover:bg-gray-50 col-span-2"
                    title="Jump to first marked for review"
                  >
                    Marked for review: <span className="font-semibold">{statusCounts.marked}</span>
                  </button>
                </div>
                <label className="mt-4 flex items-center gap-2 text-sm text-slate-800">
                  <input
                    type="checkbox"
                    checked={submitConfirmed}
                    onChange={(e) => setSubmitConfirmed(e.target.checked)}
                  />
                  I have reviewed my attempt summary and want to submit.
                </label>
                <div className="mt-5 flex justify-end gap-2">
                  <button
                    type="button"
                    onClick={() => setShowSubmitConfirm(false)}
                    className="rounded bg-gray-200 px-4 py-2 text-sm font-semibold text-slate-900 hover:bg-gray-300"
                  >
                    Not yet
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setShowSubmitConfirm(false);
                      setSubmitConfirmed(false);
                      handleSubmit();
                    }}
                    disabled={!submitConfirmed}
                    className={`rounded px-4 py-2 text-sm font-semibold text-white ${
                      submitConfirmed ? 'bg-green-600 hover:bg-green-700' : 'bg-green-300 cursor-not-allowed'
                    }`}
                  >
                    Yes, submit
                  </button>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default AssessmentPage;
