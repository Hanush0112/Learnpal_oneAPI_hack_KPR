import os
import re
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from groq import Groq

# Load API key from .env file
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Flask app setup
app = Flask(__name__)
app.secret_key = 'your_secret_key' 
messages = []

# Function to clean and format generated questions
def clean_question(question):
    cleaned_question = " ".join(question.split())
    cleaned_question = re.sub(r'\d\.\s*', '', cleaned_question)
    return cleaned_question

# Function to generate a unique question using Groq API
def generate_unique_question(content):
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": content}],
        model="llama3-8b-8192",
    )
    question = response.choices[0].message.content
    return clean_question(question)

# Function to generate questions for each subject
def generate_subject_questions(subject, num_questions):
    questions = []
    for _ in range(num_questions):
        question = generate_unique_question(f"Give ONE MCQ question with 4 options (a, b, c, d) on {subject}. Only provide the question and the options without revealing the correct answer.")
        questions.append(question)
    return questions

# IQ Test generation route
@app.route('/iq_test', methods=['GET', 'POST'])
def iq_test():
    if request.method == 'POST':
        # When user submits the IQ test
        user_answers = request.form.getlist('answer')
        session['user_answers'] = user_answers
        return redirect(url_for('iq_results'))

    # Define subjects and number of questions
    subjects = ['math', 'physics', 'chemistry', 'biology']
    total_questions = 15  # Total questions to generate
    questions_per_subject = total_questions // len(subjects)

    # Generate questions for each subject
    iq_questions = []
    for subject in subjects:
        iq_questions.extend(generate_subject_questions(subject, questions_per_subject))

    return render_template('IQ.html', questions=iq_questions)

# IQ Test Results route
@app.route('/iq_results', methods=['GET'])
def iq_results():
    user_answers = session.get('user_answers', [])
    return render_template('results.html', user_answers=user_answers)

# Route for educational questions
@app.route('/test_setup', methods=['GET', 'POST'])
def test_setup():
    if request.method == 'POST':
        subject = request.form['subject']
        grade = request.form['grade']
        num_questions = int(request.form['num_questions'])

        session['subject'] = subject
        session['grade'] = grade
        session['num_questions'] = num_questions
        session['questions'] = []
        session['user_answers'] = []
        session['explanations'] = []

        return redirect(url_for('questions', q_num=1))

    return render_template('test_setup.html')

# Step 2: Display and handle individual questions
@app.route('/questions/<int:q_num>', methods=['GET', 'POST'])
def questions(q_num):
    if request.method == 'POST':
        selected_answer = request.form['answer']
        user_answers = session.get('user_answers', [])
        user_answers.append(selected_answer)
        session['user_answers'] = user_answers

        questions = session.get('questions', [])
        current_question = questions[-1]

        # Generate the correct answer using Groq API
        answer_key_response = generate_unique_question(f"What is the correct answer for this MCQ: {current_question} in a single character (a, b, c, or d)?")
        answer_key = answer_key_response.strip()

        # Generate explanation using Groq API
        explanation_response = generate_unique_question(f"My answer is {selected_answer} for the question {current_question} with the correct answer being {answer_key}. If my answer is correct, do not elaborate. If my answer is wrong, explain clearly why.")
        explanation = explanation_response.strip()

        explanations = session.get('explanations', [])
        explanations.append(explanation)
        session['explanations'] = explanations

        if q_num < session['num_questions']:
            return redirect(url_for('questions', q_num=q_num + 1))
        else:
            return redirect(url_for('answers'))

    # Generate a new question for the user
    subject = session['subject']
    grade = session['grade']
    questions = session.get('questions', [])

    while True:
        new_question = generate_unique_question(f"Give ONE MCQ question with 4 options (a, b, c, d) on {subject} for grade {grade}. Only provide the question and the options without revealing the correct answer.")
        if new_question not in questions:
            questions.append(new_question)
            session['questions'] = questions
            break

    return render_template('test.html', question=new_question, q_num=q_num)

# Step 3: Display final answers and explanations, and calculate score
@app.route('/answers', methods=['GET'])
def answers():
    questions = session.get('questions')
    user_answers = session.get('user_answers')
    explanations = session.get('explanations')
    correct_answers = []
    score = 0

    # Validate user answers and calculate the score
    for i, question in enumerate(questions):
        correct_answer = generate_unique_question(f"What is the correct answer for this MCQ: {question} in a single character (a, b, c, or d)?").strip()
        correct_answers.append(correct_answer)

        # Check if user's answer is correct
        if user_answers[i] == correct_answer:
            score += 1

    total_questions = len(questions)
    percentage_score = (score / total_questions) * 100

    return render_template('result.html', 
                           questions=questions, 
                           user_answers=user_answers, 
                           explanations=explanations, 
                           correct_answers=correct_answers, 
                           score=score, 
                           total_questions=total_questions, 
                           percentage_score=percentage_score)

# Flask Routes for additional functionalities
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/course')
def page2():
    return render_template('course.html')

@app.route('/profile', methods=['GET'])
def profile():
    # Fetch user data from session (or database)
    user_name = session.get('user_name', 'Guest')
    user_email = session.get('user_email', 'Not provided')
    user_phone = session.get('user_phone', 'Not provided')
    user_grade = session.get('user_grade', 'Not provided')

    return render_template('profile.html', 
                           user_name=user_name,
                           user_email=user_email,
                           user_phone=user_phone,
                           user_grade=user_grade)


@app.route('/stats')
def page6():
    return render_template('stats.html')

@app.route('/login_register')
def page7():
    return render_template('login_register.html')

# Chatbot page
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html', messages=messages)

# Route to handle chatbot responses
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['input']
    groq_response = generate_unique_question(user_input + " and provide a detailed explanation.")
    
    messages.append({'sender': 'user', 'text': user_input})
    messages.append({'sender': 'bot', 'text': groq_response})
    
    return jsonify({'response': groq_response})

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        grade = request.form['grade']

        # Update session or database with new data
        session['user_name'] = name
        session['user_email'] = email
        session['user_phone'] = phone
        session['user_grade'] = grade

        # Redirect to profile after updating
        return redirect(url_for('profile'))

    # If GET request, render the edit form with current user data
    return render_template('edit_profile.html',
                           user_name=session.get('user_name', ''),
                           user_email=session.get('user_email', ''),
                           user_phone=session.get('user_phone', ''),
                           user_grade=session.get('user_grade', ''))
 

# Main app runner
if __name__ == '__main__':
    app.run(debug=True)
