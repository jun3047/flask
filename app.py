from flask import Flask, render_template, request, jsonify
import dialog 
import google.cloud.dialogflow_v2 as dialogflow
import json

app = Flask(__name__)

@app.route("/")
def project_1():
    return render_template('project_1.html')

@app.route("/chatpage")
def chatpage():
    return render_template('chat_page.html')

@app.route("/get_answer", methods=['POST'])
def get_answer():
    question = request.form.get('question')  # 사용자의 질문을 가져옵니다.

    answer = dialog.get_answer_form_server(question)
    print(answer)

    return jsonify({'answer': answer})

if __name__ == "__main__":
    app.run()
