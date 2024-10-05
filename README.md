This is meant to be a learning companion to automatically tailor to user's level of experience all while the user uses it as a normal application.
Uses: Gemini API 
# LearnPal

Welcome to **LearnPal**, an innovative web application designed to enhance learning experiences for students of all ages. LearnPal incorporates a variety of features tailored to meet the educational needs of individuals by providing personalized learning paths, skill assessments, and resources based on their age and grade level.

## Features

### 1. Skill Tests
- **Dynamic IQ Tests**: Generate personalized IQ tests with multiple-choice questions across various subjects such as Math, Physics, Chemistry, and Biology.
- **Real-Time Feedback**: Receive instant feedback on test results, including explanations for correct and incorrect answers.

### 2. Personalized Chatbot
- **Tailored Assistance**: Our chatbot provides customized responses based on user input, age, and grade. It can answer questions and explain topics in detail, enhancing understanding and retention.

### 3. Syllabus-Based Content Generation
- **Grade-Specific Syllabus**: Users can select topics aligned with their educational syllabus. LearnPal generates relevant content to aid their studies.
- **Structured Learning Path**: Based on the chosen topics, the app curates learning materials and resources.

### 4. Video Lessons
- **Curated Educational Videos**: Access video lessons for specific topics from trusted sources, enriching the learning experience through multimedia content.
  
### 5. Statistics & Progress Tracking
- **Performance Metrics**: Users can view their performance over time, including test scores and progress in various subjects, helping them identify strengths and areas for improvement.

## Technology Stack

- **Frontend**: Flask (Python), HTML, CSS, JavaScript
- **Backend**: Flask (Python) for API and routing
- **Database**: MongoDB for storing user profiles, test details, and learning materials.
- **APIs**: Groq API for generating questions and content dynamically.

## Installation

1. **Clone the Repository**
   git clone https://github.com/Hanush0112/Learnpal_oneAPI_hack_KPR.git
   cd LearnPal
   
2.**Set Up Environment**
Create a .env file in the root directory and add your Groq API key:
GROQ_API_KEY=your_api_key

3.**Install Dependencies**
Make sure you have Python and pip installed. Then, run:
pip install -r requirements.txt

4.**Start the Application**
python app.py
Open your web browser and go to http://127.0.0.1:5000/.

**Usage**
-Navigate through the app using the navigation bar to access different features.
-Use the Skill Tests section to take dynamic tests.
-Interact with the Chatbot for personalized help.
-Explore the Syllabus to find content tailored to your current studies.
-Watch Video Lessons for better understanding of complex topics.

**Contributing**
-Contributions are welcome! If you'd like to contribute to LearnPal, please follow these steps:
1Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes.
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature-branch).
Open a pull request.

**License**
This project is licensed under the MIT License - see the LICENSE file for details.

**Acknowledgments**
Special thanks to Groq for their API services.
Thanks to the creators of MongoDB for their database solutions.
For any inquiries or issues, feel free to open an issue in this repository.

Happy Learning!

### Key Highlights:
- This README outlines the purpose of the **LearnPal** application and its features comprehensively.
- Installation and usage instructions make it easy for users to get started.
- Contributing guidelines encourage community participation.
- License and acknowledgments provide transparency and credit to utilized resources.

Feel free to modify any part as needed!
