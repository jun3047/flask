import os
import google.cloud.dialogflow_v2 as dialogflow
import json

def get_answer_form_server(our_query):
   
   with open('private_key.json') as f:
      data = json.load(f)

   result = ""

   print("our_query:", our_query)
   
   os.environ["GOOGLE_APPLICATION_CREDENTIALS"] ='private_key.json'
   DIALOGFLOW_PROJECT_ID = data['project_id']
   DIALOGFLOW_LANGUAGE_CODE ='ko'
   SESSION_ID ='me'
   session_client = dialogflow.SessionsClient()
   session = session_client.session_path(DIALOGFLOW_PROJECT_ID,SESSION_ID)
   our_input = dialogflow.types.TextInput(text=our_query,language_code=DIALOGFLOW_LANGUAGE_CODE)

   query = dialogflow.types.QueryInput(text=our_input)

   print("session:", session)
   print("query:", query)
   response = session_client.detect_intent(session=session,query_input=query)   

   print("response.query_result.intent.display_name:", response.query_result.intent.display_name)


   if response.query_result.intent.display_name =='WhatisMENU':
      lst=list(response.query_result.parameters.values())
      timeslot=lst[0]
      date=lst[1]
      date=date[5:10:1]
      location=lst[2]

      if timeslot=='' or date=='' or location=='':
         return response.query_result.fulfillment_text, result


      print("~~~~~~", timeslot,date,location)

      if location=='학생식당':
         with open('data.json', 'r',encoding='utf8') as f:
            json_data = json.load(f)
            for v in json_data[date][timeslot]['메뉴']:
               result += v['구분'] + str(v['가격'])+"원" + "\n" + ", ".join(v['상세메뉴']) + "\n"

      else:
         with open('teacher_data.json', 'r',encoding='utf8') as f:
            json_data = json.load(f)
            for v in json_data[date]:
               if timeslot in v['구분']:
                  result += v['구분'] + str(v['가격'])+"원" + "\n" +  ", ".join(v['메뉴']) + "\n"
            
   elif response.query_result.intent.display_name=='academicCalendar':
      lst=list(response.query_result.parameters.values())
      semester=lst[0]
      type=lst[1]
      with open('AcademicCalendar.json', 'r',encoding='utf8') as f:
         json_data = json.load(f)
         for _data in json_data[semester][type].keys():
            result += _data + "\n"
            
   return response.query_result.fulfillment_text, result
