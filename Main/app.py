from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyCVajDsPhoXTmgh3I3ibR_nbD_6yn7mh8U")

# Initialize the model (replace "gemini-1.5-flash" with your actual model name)
model = genai.GenerativeModel("gemini-1.5-flash")


app = Flask(__name__)

def get_gemini_response(user_input):
    prompt = user_input + " and provide a detailed explanation. Use <br> after every full stop."
    
    response = model.generate_content(prompt)
    
    if response._result.candidates and response._result.candidates[0].content.parts:
        generated_text = response._result.candidates[0].content.parts[0].text
        formatted_output = generated_text.replace('.','.\n')
        
    else:
        formatted_output = "Sorry, I couldn't generate a response."
    
    return formatted_output


messages = []


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/course')
def page2():
    return render_template('course.html')

@app.route('/test_setup')
def page3():
    return render_template('test_setup.html')


@app.route('/profile')
def page5():
    return render_template('profile.html')

@app.route('/stats')
def page6():
    return render_template('stats.html')

@app.route('/login_register')
def page7():
    return render_template('login_register.html')


@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html', messages=messages)

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['input']  
    gemini_response = get_gemini_response(user_input)  
    
    messages.append({'sender': 'user', 'text': user_input})
    messages.append({'sender': 'bot', 'text': gemini_response})
    
    return jsonify({'response': gemini_response})  

if __name__ == '__main__':
    app.run(debug=True)
