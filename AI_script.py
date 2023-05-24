import openai
import pandas as pd
from collections import Counter
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai.api_key = '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'

@app.route('/execute-script', methods=['POST'])
def execute_script():
    csv_file = request.files['csvFile']
    csv_file.save('uploads/emails.csv')

    emails_df = pd.read_csv('uploads/emails.csv')
    original_emails = emails_df['Content']
    email_subjects = emails_df['Subject']

    tasks = []
    common_subjects = []

    # Find common subjects
    subject_counts = Counter(email_subjects)
    for subject, count in subject_counts.most_common():
        if count > 1:
            common_subjects.append(subject)

    # Process emails and create tasks
    for email, subject in zip(original_emails, email_subjects):
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Convert the following email into a task for a to-do list and suggest a priority level (high, medium, low)."},
            {"role": "user", "content": email}
        ]

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            max_tokens=1000
        )

        task = response['choices'][0]['message']['content']

        # Check if the subject is common among the emails
        if subject in common_subjects:
            task += f" [Subject: {subject}]"

        tasks.append(task)

    # Concatenate tasks and emails into a single string
    task_text = "\n".join(tasks)
    email_text = "\n".join(original_emails)
    all_text = task_text + "\n" + email_text

    # Get user question from the request payload
    user_question = request.form['question']

    # Add user question to messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant that can answer questions about tasks and emails."},
        {"role": "user", "content": all_text + "\nUser Question: " + user_question}
    ]

    # Generate AI response
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        max_tokens=1000
    )

    answer = response['choices'][0]['message']['content']
    
    # Return the AI response as a JSON object
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(port=3000)
