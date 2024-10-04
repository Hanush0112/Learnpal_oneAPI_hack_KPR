import google.generativeai as genai
import os
from dotenv import load_dotenv
from answekey import extract_letters

load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")
model2 = genai.GenerativeModel("gemini-1.0-pro")
subject="Math"
grade="12"
Time="15"
answers=['a','a','c','b','c','a','b','b','a','d']
def generate():
    response = model.generate_content("Give MCQ test (only ONE correct option each) on "+subject+"for grade"+grade+"to be done reasonably in "+Time+"minutes. Adjust number of questions accordingly.Do not include answer key.").text
    answe2= model2.generate_content("What is the answer key of"+response+"in a python list form, with each element being single character a,b,c or d").text
    check1= model.generate_content("My answers are "+str(answers)+"for the questions"+response+"with answer key"+str(answe2)+"Explain each question, and how my option is either right or wrong").text
    print(response)
    #answer = extract_letters(answe2)
    return response,answe2,check1 

q,a,c=generate()
print(q,"     ",a,"     ",c)