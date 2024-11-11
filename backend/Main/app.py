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

    for key, values in data['feedback1'].items():
        idx = int(key)
        total_marks += 1
        selected_answer = int(data['selectedOptions'][idx])
        correct_answer = int(data['correctOptions'][key])

        if selected_answer == correct_answer:
            marks_scored += 1

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

if __name__ == '__main__':
    app.run(debug=True)


