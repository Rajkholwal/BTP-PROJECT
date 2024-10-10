import Generator

def generateAssessment(tags,numQuestions,level):
    print("hello")
    numQuestions = int(numQuestions)
    questionDetails = []
    for question_num in range(numQuestions):
        images = []
        return_value = Generator.generate_question(level,tags)
        question, options, answer = return_value[:3]
        if len(return_value) == 4: images = return_value[3]
        newQuestionDetail = {"question": question, "options": options, "answer": answer, "images": images}
        questionDetails.append(newQuestionDetail)
    return questionDetails
