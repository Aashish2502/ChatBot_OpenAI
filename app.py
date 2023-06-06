from flask import Flask, render_template, request
import openai
import os
from diseases import diseases

app = Flask(__name__, static_url_path='/static')

api_key = os.getenv('API_KEY')


openai.api_key = api_key

@app.route('/')
def index():

    return render_template('index.html', conditions = diseases)


@app.route('/chat', methods=['POST'])
def chat():
    condition = request.form['condition']
    severity = request.form['severity']

    
    res = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f'Condition: {condition}, Severity: {severity}\nUser:',
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    reply = res.choices[0].text.strip()
    
    return render_template('reply.html', condition=condition, severity=severity, reply=reply)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
