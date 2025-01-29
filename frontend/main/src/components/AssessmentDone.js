import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import jsPDF from 'jspdf';
import LoadingResult from './LoadingResult';
import UpperNav from './UpperNav';

const AssessmentDone = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const { questions, marks, loggedInName, loggedInEmail,selectedOptions,timeSpentPerQuestion } = useLocation().state;
    const marksScored = marks[0];
    const totalMarks = marks[1];
    const seconds = marks[2];
    const percentage1 = (marksScored / totalMarks) * 100;
    const percentage = percentage1.toFixed(2);


    const generatePDF = () => {
        const pdf = new jsPDF();
        const xOffset = 20;
        let yOffset = 30;

        pdf.setFontSize(16);
        pdf.text("Questions and Answers", pdf.internal.pageSize.width / 2, yOffset, { align: 'center' });
        yOffset += 20;

        const convertSvgToPng = (svgString, width, height) => {
            return new Promise((resolve, reject) => {
                const canvas = document.createElement('canvas');
                const scaleFactor = 2; // Higher resolution for sharper image
                canvas.width = width * scaleFactor;
                canvas.height = height * scaleFactor;
                const ctx = canvas.getContext('2d');

                const img = new Image();
                const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
                const url = URL.createObjectURL(svgBlob);

                img.onload = () => {
                    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                    URL.revokeObjectURL(url);
                    resolve(canvas.toDataURL('image/png', 1.0)); // Save with full quality
                };

                img.onerror = reject;
                img.src = url;
            });
        };
        
        const processSvg = async (svgData) => {
            let svgString, width, height;

            if (typeof svgData === 'string') {
                svgString = svgData;
            } else if (svgData instanceof SVGElement) {
                svgString = new XMLSerializer().serializeToString(svgData);
            } else {
                console.error("Invalid SVG data format");
                return null;
            }

            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = svgString;
            const svgElement = tempDiv.querySelector('svg');

            if (svgElement) {
                width = parseFloat(svgElement.getAttribute('width')) || 100;
                height = parseFloat(svgElement.getAttribute('height')) || 100;

                if (!width || !height) {
                    const viewBox = svgElement.getAttribute('viewBox');
                    if (viewBox) {
                        const [, , vbWidth, vbHeight] = viewBox.split(' ').map(parseFloat);
                        width = width || vbWidth || 100;
                        height = height || vbHeight || 100;
                    }
                }
            } else {
                width = 100;
                height = 100;
            }

            try {
                const pngDataUrl = await convertSvgToPng(svgString, width, height);
                return { dataUrl: pngDataUrl, width: width / 2, height: height / 2 }; // Scale for PDF clarity
            } catch (error) {
                console.error("Error converting SVG to PNG:", error);
                return null;
            }
        };

        const addQuestionToPdf = async (q, index) => {
            const pageHeight = pdf.internal.pageSize.height;
            const lineHeight = 10;
            const spaceNeeded = lineHeight * (q.options.length + 3);

            if (yOffset + spaceNeeded > pageHeight) {
                pdf.addPage();
                yOffset = 30;
            }

            pdf.setFontSize(12);
            const lines = pdf.splitTextToSize(`Q ${index + 1}: ${q.question}`, pdf.internal.pageSize.width - 2 * xOffset);
            pdf.text(xOffset, yOffset, lines);
            yOffset += lineHeight * lines.length + 5; // Space after question

            // Add each image below the question
            if (q.images && q.images.length > 0) {
                for (let i = 0; i < q.images.length; i++) {
                    const svgData = await processSvg(q.images[i]);
                    if (svgData) {
                        const scaledHeight = svgData.height * 0.8; // Decrease height by 20%
                        pdf.addImage(svgData.dataUrl, 'PNG', xOffset, yOffset, svgData.width, scaledHeight);
                        yOffset += scaledHeight + 8; // Small gap after each image
                    } else {
                        pdf.text("Error: Unable to load image", xOffset, yOffset);
                        yOffset += lineHeight;
                    }
                }
            }

            // Add options below the images
            q.options.forEach((option, optionIndex) => {
                const optionLines = pdf.splitTextToSize(`${String.fromCharCode(65 + optionIndex)}. ${option}`, pdf.internal.pageSize.width - 2 * xOffset - 10);
                pdf.text(xOffset + 10, yOffset, optionLines);
                yOffset += lineHeight * optionLines.length + 1; // Small gap after each option
            });

            pdf.setFontSize(10);
            pdf.setTextColor(0, 150, 0);
            const answerLines = pdf.splitTextToSize(`Correct Answer: ${q.answer}`, pdf.internal.pageSize.width - 2 * xOffset - 10);
            pdf.text(xOffset + 10, yOffset, answerLines);
            yOffset += lineHeight * answerLines.length + 10;

            pdf.setTextColor(0, 0, 0);
            pdf.setFontSize(12);
            if (index < questions.length - 1) {
                pdf.addPage();
                yOffset = 30;
            }
        };

        const generatePdfContent = async () => {
            for (let i = 0; i < questions.length; i++) {
                await addQuestionToPdf(questions[i], i);
            }
            pdf.save('questions.pdf');
        };

        generatePdfContent();
    };
    console.log("times",timeSpentPerQuestion);
    useEffect(() => {
        setTimeout(() => {
            setLoading(false);
        }, 3000);
    }, []);

    // Save data to the backend
    const convertedTimeSpentPerQuestion = timeSpentPerQuestion.map(ms => `${(ms / 1000)}s`);

    const selectedOpt = questions.map((question, index) => ({

        selectedOption: question.options[selectedOptions[index]] || 'Not answered',
    }));
    const saveAssessmentData = async () => {
        const data = {
            questions,
            marks,
            seconds,
            selectedOpt,
            timeSpentPerQuestion: convertedTimeSpentPerQuestion, 
        };

        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/save-assessment`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                const result = await response.json();
                console.log('Data saved:', result);
            } else {
                console.error('Failed to save data:', response.statusText);
            }
        } catch (error) {
            console.error('Error saving data:', error);
        }
    };

    useEffect(() => {
        setTimeout(() => {
            setLoading(false);
        }, 3000);

        saveAssessmentData(); // Trigger data save when the component mounts
    }, []);

    return (
        <div>
            {loading ? (
                <LoadingResult />
            ) : (
                <>
                    <UpperNav name={loggedInName} email={loggedInEmail} />
                    <div className="bg-white py-24 sm:py-32">
                        <div className="mx-auto max-w-7xl px-6 lg:px-8">
                            <dl className="grid grid-cols-1 gap-x-8 gap-y-16 text-center lg:grid-cols-4">
                                <div className="mx-auto flex max-w-xs flex-col gap-y-4">
                                    <dt className="text-base leading-7 text-gray-600">Total questions</dt>
                                    <dd className="order-first text-3xl font-semibold tracking-tight text-gray-900 sm:text-5xl">{totalMarks}</dd>
                                </div>
                                <div className="mx-auto flex max-w-xs flex-col gap-y-4">
                                    <dt className="text-base leading-7 text-gray-600">Questions solved correctly</dt>
                                    <dd className="order-first text-3xl font-semibold tracking-tight text-gray-900 sm:text-5xl">{marksScored}</dd>
                                </div>
                                <div className="mx-auto flex max-w-xs flex-col gap-y-4">
                                    <dt className="text-base leading-7 text-gray-600">Percentage secured</dt>
                                    <dd className="order-first text-3xl font-semibold tracking-tight text-gray-900 sm:text-5xl">{percentage}%</dd>
                                </div>
                                <div className="mx-auto flex max-w-xs flex-col gap-y-4">
                                    <dt className="text-base leading-7 text-gray-600">Time taken</dt>
                                    <dd className="order-first text-3xl font-semibold tracking-tight text-gray-900 sm:text-5xl">{seconds}</dd>
                                </div>
                            </dl>
                        </div>
                        <br />
                        <div className="mt-10 flex items-center justify-center gap-x-6">
                            <a onClick={generatePDF} className="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                                Download complete PDF with answers
                            </a>
                            <button onClick={() => navigate('/')} className="text-sm font-semibold leading-6 text-gray-900">
                                Attempt another quiz<span aria-hidden="true">→</span>
                            </button>
                            <button
                                onClick={() => navigate('/review-assessment', { state: { questions, marks, seconds,selectedOptions, timeSpentPerQuestion } })}
                                className="bg-green-500 text-white font-semibold leading-6 px-4 py-2 rounded transition duration-200 hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
                            >
                                Review Assessment<span aria-hidden="true">→</span>
                            </button>

                        </div>
                    </div>
                </>
            )}
        </div>
    );
}

export default AssessmentDone;
