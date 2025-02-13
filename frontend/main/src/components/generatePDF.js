import jsPDF from 'jspdf';

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

const generatePDF = async (questions) => {
    const pdf = new jsPDF();
    const xOffset = 20;
    let yOffset = 30;

    pdf.setFontSize(16);
    pdf.text("Questions and Answers", pdf.internal.pageSize.width / 2, yOffset, { align: 'center' });
    yOffset += 20;

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

        if (q.images && q.images.length > 0) {
            for (let i = 0; i < q.images.length; i++) {
                const svgData = await processSvg(q.images[i]);
                if (svgData) {
                    const scaledHeight = svgData.height * 0.8;
                    pdf.addImage(svgData.dataUrl, 'PNG', xOffset, yOffset, svgData.width, scaledHeight);
                    yOffset += scaledHeight + 8; 
                } else {
                    pdf.text("Error: Unable to load image", xOffset, yOffset);
                    yOffset += lineHeight;
                }
            }
        }

        q.options.forEach((option, optionIndex) => {
            const optionLines = pdf.splitTextToSize(`${String.fromCharCode(65 + optionIndex)}. ${option}`, pdf.internal.pageSize.width - 2 * xOffset - 10);
            pdf.text(xOffset + 10, yOffset, optionLines);
            yOffset += lineHeight * optionLines.length + 1; 
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

    for (let i = 0; i < questions.length; i++) {
        await addQuestionToPdf(questions[i], i);
    }

    pdf.save('questions.pdf');
};

export default generatePDF;
