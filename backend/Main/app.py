# from flask import Flask, render_template, request, jsonify, send_from_directory, send_file, url_for, redirect
# from flask_cors import CORS, cross_origin
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from main import main
# import os
# import io
# from generateAssessment import generateAssessment
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# import googleapiclient.discovery

# SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# SPREADSHEET_ID = '1KlwPwg3QgPrYsGJNNYjw31NDJ5Z7gkPX8a-RLqQbF0o'

# def get_google_sheets_service():
#     creds = None
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json",SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                  "credentials.json", SCOPES
#             )
#             creds = flow.run_local_server(port=0)
#         with open("token.json","w") as token:
#             token.write(creds.to_json())
#     service = googleapiclient.discovery.build('sheets', 'v4', credentials=creds)
#     return service

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# @app.route("/")
# def starting():
#     return "Server is running"

# @app.route('/submit_quiz', methods=['POST'])
# @cross_origin(origin='*')
# def submit_quiz():
#     data = request.json  
    
#     print('Received quiz data for PDF generation:', data)

#     ans = main(data['tags'],data['numQuestions'],data['level'])

#     return jsonify({'message': 'Quiz submitted successfully'})

# @app.route('/startAssessment', methods=['POST'])
# @cross_origin(origin='*')
# def startAssessment():
#     data = request.json
#     print('Received quiz data to generate assessment:', data)

#     questionDetails = generateAssessment(data['tags'], data['numQuestions'], data['level'])
#     print(questionDetails)

#     return jsonify({'questions': questionDetails})
    
# @app.route('/submit_assessment', methods=['POST'])
# @cross_origin(origin='*')
# def submit_assessment():
#     data = request.json
#     print('Recieved assessment data')
#     print(data)
#     sheets_service = get_google_sheets_service()
#     range_ = 'Sheet1'
    
#     firstdone = 0
#     total_marks = 0
#     marks_scored = 0
#     values = [['Name:',data['name'],'Email:',data['email'],'Type:',data['type']]]
#     print(data)
#     result = sheets_service.spreadsheets().values().get(
#             spreadsheetId=SPREADSHEET_ID, range=range_
#         ).execute()
#     values_in_sheet = result.get('values', [])
#     last_row_index = len(values_in_sheet)
#     last_row_index = last_row_index + 1
#     new_range = f'{range_}!A{last_row_index + 1}'
#     sheets_service.spreadsheets().values().update(
#         spreadsheetId=SPREADSHEET_ID, range=new_range,
#         body={'values': values}, valueInputOption='RAW'
#     ).execute()
    
#     values = [['index','question','option-A','option-B','option-C','option-D','answer','Time taken per question','feedback']]
#     result = sheets_service.spreadsheets().values().get(
#             spreadsheetId=SPREADSHEET_ID, range=range_
#     ).execute()
#     values_in_sheet = result.get('values', [])
#     last_row_index = len(values_in_sheet)
#     new_range = f'{range_}!A{last_row_index + 1}'
#     sheets_service.spreadsheets().values().update(
#             spreadsheetId=SPREADSHEET_ID, range=new_range,
#             body={'values': values}, valueInputOption='RAW'
#     ).execute()
    
#     for key,values in data['feedback1'].items():
#         idx = int(key)
#         total_marks = total_marks + 1
#         if int(data['selectedOptions'][idx]) == int(data['correctOptions'][key]):
#             marks_scored = marks_scored + 1
            
#         values = [[idx+1,data['questionBodies'][idx]['question'],data['questionBodies'][idx]['options'][0],data['questionBodies'][idx]['options'][1],data['questionBodies'][idx]['options'][0],data['questionBodies'][idx]['options'][1],data['questionBodies'][idx]['answer'],data['individualTimeTaken'][idx],data['feedback1'][key]]]
#         result = sheets_service.spreadsheets().values().get(
#             spreadsheetId=SPREADSHEET_ID, range=range_
#         ).execute()
#         values_in_sheet = result.get('values', [])
#         last_row_index = len(values_in_sheet)
#         new_range = f'{range_}!A{last_row_index + 1}'
#         sheets_service.spreadsheets().values().update(
#             spreadsheetId=SPREADSHEET_ID, range=new_range,
#             body={'values': values}, valueInputOption='RAW'
#         ).execute()
        
#     values = [['Total Questions:',total_marks,'Marks Scored:',marks_scored,'Total time taken:',data['timeTaken']]]
#     result = sheets_service.spreadsheets().values().get(
#             spreadsheetId=SPREADSHEET_ID, range=range_
#         ).execute()
#     values_in_sheet = result.get('values', [])
#     last_row_index = len(values_in_sheet)
#     new_range = f'{range_}!A{last_row_index + 1}'
#     sheets_service.spreadsheets().values().update(
#         spreadsheetId=SPREADSHEET_ID, range=new_range,
#         body={'values': values}, valueInputOption='RAW'
#     ).execute()
#     last_row_index = last_row_index+1

#     return jsonify({'total_marks': total_marks, 'marks_scored': marks_scored})


# @app.route('/pdf-files/<filename>', methods=['GET'])
# def get_pdf(filename):
#     pdf_directory = './PDF/'  # Update with the actual path to your PDF files
#     return send_from_directory(pdf_directory, filename)

# @app.route('/pdf-files', methods=['GET'])
# def get_pdf_files():
#     print("started it")
#     pdf_files = [file for file in os.listdir('./PDF') if file.endswith('.pdf')]
#     return jsonify(pdf_files)


# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, jsonify, send_from_directory, send_file, url_for, redirect
from flask_cors import CORS, cross_origin
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from main import main
import os

import io
from generateAssessment import generateAssessment

from datetime import datetime


# MongoDB Connection
from pymongo import MongoClient
client = MongoClient('mongodb+srv://kumarchspiyush:nGyCgIRvLThU73ix@cluster0.fdcer.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0') 
db = client['quizApp']  # Database name
collection = db['quizResults']  # Collection name
users_collection = db['users']  # Collection to store user data
assessments_collection = db['assessments'] 

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/")
def starting():
    return "Server is running"

@app.route('/submit_quiz', methods=['POST'])
@cross_origin(origin='*')
def submit_quiz():
    data = request.json  
    print('Received quiz data for PDF generation:', data)

    ans = main(data['tags'], data['numQuestions'], data['level'])
    return jsonify({'message': 'Quiz submitted successfully'})

@app.route('/startAssessment', methods=['POST'])
@cross_origin(origin='*')
def startAssessment():
    data = request.json
    print('Received quiz data to generate assessment:', data)

    questionDetails = generateAssessment(data['tags'], data['numQuestions'], data['level'])
    print(questionDetails)

    return jsonify({'questions': questionDetails})
   
@app.route('/submit_assessment', methods=['POST'])
def submit_assessment():
    data = request.json
    print('Received assessment data:', data)
    
    total_marks = 0
    marks_scored = 0

    # data['feedback1'] is a dict whose keys match question indices
    # data['selectedOptions'] is an array
    # data['correctOptions'] is also a dict or object in JS (use the question index as a key)
    for key in data['feedback1'].keys():
        idx = int(key)
        total_marks += 1

        # selected_answer = int(data['selectedOptions'][idx])
        # # Make sure to convert the correct option from data['correctOptions'][idx] 
        # # (which might be a string key if you set it that way)
        # correct_answer = int(data['correctOptions'][key])

        # if selected_answer == correct_answer:
        #     marks_scored += 1

    return jsonify({'total_marks': total_marks, 'marks_scored': marks_scored})

@app.route('/pdf-files/<filename>', methods=['GET'])
def get_pdf(filename):
    pdf_directory = './PDF/'  # Update with the actual path to your PDF files
    return send_from_directory(pdf_directory, filename)

@app.route('/pdf-files', methods=['GET'])
def get_pdf_files():
    print("Started fetching PDF files")
    pdf_files = [file for file in os.listdir('./PDF') if file.endswith('.pdf')]
    return jsonify(pdf_files)

@app.route('/save-assessment', methods=['POST'])
def save_assessment():
    data = request.json  # Get JSON data sent from the frontend
    try:
        # Insert data into the collection
        collection.insert_one(data)
        return jsonify({"status": "success", "message": "Data saved successfully"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/auth/google', methods=['POST'])
def google_auth():
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        googlePhotoUrl = data.get("googlePhotoUrl")

        if not email:
            return jsonify({"error": "Email is required"}), 400

        # Check if user already exists
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            users_collection.update_one({"email": email}, {"$set": {"name": name, "googlePhotoUrl": googlePhotoUrl}})
        else:
            users_collection.insert_one({"name": name, "email": email, "googlePhotoUrl": googlePhotoUrl})

        return jsonify({"message": "User saved successfully", "user": {"name": name, "email": email, "googlePhotoUrl": googlePhotoUrl}}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500 


@app.route('/submit_user_assessment', methods=['POST'])
def submit_user_assessment():
    data = request.json
    print('Received assessment data:', data)

    email = data.get('email')
    if not email:
        return jsonify({"status": "error", "message": "User email is required"}), 400

    assessment_data = data.get("assessments", {})

    formatted_questions = []
    for i, q in enumerate(assessment_data.get("questionBodies", [])):
        selected_index = assessment_data["selectedOptions"][i] if i < len(assessment_data["selectedOptions"]) else None
        selected_option = q["options"][selected_index] if isinstance(selected_index, int) and 0 <= selected_index < len(q["options"]) else "Not answered"

        formatted_questions.append({
            "question": q["question"],
            "options": q["options"],
            "answer": q["options"][assessment_data["correctOptions"].get(str(i), -1)] if str(i) in assessment_data["correctOptions"] else "Unknown",
            "selectedOption": selected_option,
            "timeSpent": assessment_data.get("individualTimeTaken", [])[i] if i < len(assessment_data.get("individualTimeTaken", [])) else 0,
            "images": q.get("images", [])
        })

    assessment_entry = {
        "questions": formatted_questions,
        "submittedAt": datetime.utcnow()
    }

    print("Processed assessment entry:", assessment_entry)

    try:
        assessments_collection.update_one(
            {"email": email},
            {"$push": {"assessments": assessment_entry}},
            upsert=True
        )

        return jsonify({"status": "success", "message": "User assessment saved successfully"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500





@app.route('/get_assessments/<email>', methods=['GET'])
def get_assessments(email):
    try:
        user_data = assessments_collection.find_one({"email": email}, {"_id": 0, "assessments": 1})

        if not user_data or "assessments" not in user_data:
            return jsonify([]), 200  # Return an empty list if no assessments are found

        assessments = []
        for i, assess in enumerate(user_data["assessments"]):
            total_questions = len(assess.get("selectedOptions", []))
            correct_answers = sum(
                1 for j in range(total_questions)
                if assess["selectedOptions"][j] == assess["correctOptions"].get(j, -1)  # Fix here
            ) if total_questions else 0

            assessment_data = {
                "title": assess.get("title", f"Assessment {i + 1}"),
                "score": round(100 * correct_answers / total_questions, 2) if total_questions else 0,
                "date": assess.get("submittedAt").strftime("%Y-%m-%d %H:%M:%S") if isinstance(assess.get("submittedAt"), datetime) else "Unknown",
                "questions": assess.get("questions", []),
                "selectedOptions": assess.get("selectedOptions", []),
                "correctOptions": assess.get("correctOptions", {}),
                "individualTimeTaken": assess.get("individualTimeTaken", []),
                "options": assess.get("options", [])  # Ensure this is a **list of lists** if needed
            }
            assessments.append(assessment_data)

        return jsonify(assessments), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)




