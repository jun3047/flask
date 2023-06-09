import os
import google.cloud.dialogflow_v2 as dialogflow
import json
import PyPDF2

def print_pdf(file_path):
   pdf_file = open(file_path, 'rb')
   pdf_reader = PyPDF2.PdfReader(pdf_file)
   page = pdf_reader.pages[0]
   print(page.extract_text())
   pdf_file.close()
# JSON 파일 열기
with open('private_key.json') as f:
   data = json.load(f)


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] ='private_key.json'
DIALOGFLOW_PROJECT_ID = data['project_id']
DIALOGFLOW_LANGUAGE_CODE ='ko'
our_query =input()
SESSION_ID ='me'
session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID,SESSION_ID)
our_input = dialogflow.types.TextInput(text=our_query,language_code=DIALOGFLOW_LANGUAGE_CODE)
query = dialogflow.types.QueryInput(text=our_input)
response = session_client.detect_intent(session=session,query_input=query)
print("Dialogflow's response:",response.query_result.fulfillment_text)

while not response.query_result.all_required_params_present :
   our_query =input()
   session = session_client.session_path(DIALOGFLOW_PROJECT_ID,SESSION_ID)
   our_input = dialogflow.types.TextInput(text=our_query,language_code=DIALOGFLOW_LANGUAGE_CODE)
   query = dialogflow.types.QueryInput(text=our_input)
   response = session_client.detect_intent(session=session,query_input=query)
   response.query_result.fulfillment_text
   if response.query_result.all_required_params_present:
      break
   print("Dialogflow's response:",response.query_result.fulfillment_text)



print("Dialogflow's intent:",response.query_result.intent.display_name)
print("response.query_result.all_required_params_present:", response.query_result.all_required_params_present)

#들어간 토큰 확인.
if response.query_result.intent.display_name =='WhatisMENU':
   lst=list(response.query_result.parameters.values())
   timeslot=lst[0]
   date=lst[1]
   date=date[5:10:1]
   location=lst[2]

   print("~~~~~~", timeslot,date,location)

   if location=='학생식당':
      with open('data.json', 'r',encoding='utf8') as f:
         json_data = json.load(f)
         for v in json_data[date][timeslot]['메뉴']:
            print(v['구분'],str(v['가격'])+"원")
            print(", ".join(v['상세메뉴']))
   else:
      with open('teacher_data.json', 'r',encoding='utf8') as f:
         json_data = json.load(f)
         for v in json_data[date]:
            if timeslot in v['구분']:
               print(v['구분'],str(v['가격'])+"원")
               print(", ".join(v['메뉴']))
         
elif response.query_result.intent.display_name=='academicCalendar':
   lst=list(response.query_result.parameters.values())
   semester=lst[0]
   type=lst[1]
   with open('AcademicCalendar.json', 'r',encoding='utf8') as f:
      json_data = json.load(f)
      for data in json_data[semester][type].keys():
         print(data)
elif response.query_result.intent.display_name=='seasonInfor':
   season_file_path = 'inform(season).pdf'
   print_pdf(season_file_path)