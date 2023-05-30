import os
import google.cloud.dialogflow_v2 as dialogflow
import json

def get_answer_form_server(our_query):
   
   with open('private_key.json') as f:
      data = json.load(f)


   os.environ["GOOGLE_APPLICATION_CREDENTIALS"] ='private_key.json'
   DIALOGFLOW_PROJECT_ID = data['project_id']
   DIALOGFLOW_LANGUAGE_CODE ='ko'
   SESSION_ID ='me'
   session_client = dialogflow.SessionsClient()
   session = session_client.session_path(DIALOGFLOW_PROJECT_ID,SESSION_ID)
   our_input = dialogflow.types.TextInput(text=our_query,language_code=DIALOGFLOW_LANGUAGE_CODE)
   query = dialogflow.types.QueryInput(text=our_input)
   response = session_client.detect_intent(session=session,query_input=query)


  
   return response.query_result.fulfillment_text
