import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
import re

# Load API key
load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])

# Initialize models
model = genai.GenerativeModel("gemini-1.5-flash")
model2 = genai.GenerativeModel("gemini-1.0-pro")

# Flask app setup
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used to store session data

# Function to clean and format generated questions
def clean_question(question):
    # Remove extra newlines or multiple consecutive spaces
    cleaned_question = " ".join(question.split())
    
    # Ensure proper formatting of options (remove numbers or unintended symbols before options)
    cleaned_question = re.sub(r'\d\.\s*', '', cleaned_question)  # Remove any numbered options like '1.', '2.'
    
    return cleaned_question

# Function to generate a unique question
def generate_unique_question(subject, grade):
    # Generate a single question with options
    question = model.generate_content(
        f"Give ONE MCQ question with 4 options (a, b, c, d) on {subject} for grade {grade}. Only provide the question and the options without revealing the correct answer. No explanations or hints."
    ).text
    
    # Clean the generated question
    return clean_question(question)

# Step 1: Generate the test
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data for test generation
        subject = request.form['subject']
        grade = request.form['grade']
        num_questions = int(request.form['num_questions'])

        # Store subject, grade, and number of questions in session
        session['subject'] = subject
        session['grade'] = grade
        session['num_questions'] = num_questions
        session['questions'] = []
        session['user_answers'] = []
        session['explanations'] = []

        # Redirect to the first question
        return redirect(url_for('questions', q_num=1))

    return render_template('index.html')

# Step 2: Display and handle individual questions
@app.route('/questions/<int:q_num>', methods=['GET', 'POST'])
def questions(q_num):
    if request.method == 'POST':
        # Get the selected answer from the form
        selected_answer = request.form['answer']

        # Append the selected answer to the session list of answers
        user_answers = session.get('user_answers', [])
        user_answers.append(selected_answer)
        session['user_answers'] = user_answers  # Save back to session

        # Retrieve the generated question for explanation
        questions = session.get('questions', [])
        current_question = questions[-1]

        # Generate answer key for the current question
        answer_key = model2.generate_content(
            f"What is the correct answer for this MCQ: {current_question} in a single character (a, b, c, or d)?"
        ).text.strip()

        # Generate explanation for the current question
        explanation = model.generate_content(
            f"My answer is {selected_answer} for the question {current_question} with the correct answer being {answer_key}. If my answer is correct, do not elaborate.If my answer is wrong, explain clearly why."
        ).text

        # Store the explanation in the session
        explanations = session.get('explanations', [])
        explanations.append(explanation)
        session['explanations'] = explanations

        # Check if more questions need to be generated
        if q_num < session['num_questions']:
            return redirect(url_for('questions', q_num=q_num + 1))
        else:
            return redirect(url_for('answers'))

    # Generate a new question for GET requests
    subject = session['subject']
    grade = session['grade']
    questions = session['questions']

    # Generate a new unique question
    while True:
        new_question = generate_unique_question(subject, grade)
        if new_question not in questions:
            questions.append(new_question)
            session['questions'] = questions  # Update session with new questions
            break

    return render_template('question.html', question=new_question, q_num=q_num)

# Step 3: Display final answers and explanations
@app.route('/answers', methods=['GET', 'POST'])
def answers():
    # Retrieve the generated questions, user's answers, and explanations
    questions = session.get('questions')
    user_answers = session.get('user_answers')
    explanations = session.get('explanations')

    # Render results in the HTML page
    return render_template('results.html', questions=questions, user_answers=user_answers, explanations=explanations)

if __name__ == '__main__':
    app.run(debug=True)
