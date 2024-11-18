import os
import openai
import pdfplumber
import ast
import pickle
from collections import defaultdict
from profile import Candidate

openai.api_key = os.environ['OPENAI_API_KEY']
SYSTEM_MESSAGE_TEXT_FILE = "system_message.txt"
JOB_DETAILS_TEXT_FILE = "job_details.txt"
DELIMITER = "####"

#depending on input of user
cv_folder_path = "/Users/danielnamatinia/Desktop/CV"

client = openai.OpenAI()

#list of Candidate objects
candidates = []

def main():
    load_candidates()
    for file in os.listdir(cv_folder_path):
        pdf_path = cv_folder_path + "/" + file
        #reads and stores system_message - constant, and job details - variable depending on job.
        system_message= read_txt_file(SYSTEM_MESSAGE_TEXT_FILE, read_txt_file(JOB_DETAILS_TEXT_FILE))
        #reads the CV using pdfplumber library
        user_message= extract_text(pdf_path)
        #gets the response from the GPT API using relevant information, as a machine readible dict
        output_dict = prompt_gpt(user_message, system_message)
        try:
            output_dict=ast.literal_eval(output_dict)
        except SyntaxError:
            #it wasnt machine readible - GPT's mistake
            print("The output is not a valid JSON")
        # turns the dict with relevant information about the candidate to an instance of the Candidate object.
        parse_dict_to_candidate(output_dict)
        #preview.
    store_candidates(candidates)

def store_candidates(candidates):
    with open("candidates.pkl", "wb") as file:
        pickle.dump(candidates, file)

def load_candidates():
    try:
        with open("candidates.pkl", "wb") as file:
            global candidates
            candidates = pickle.load(file)
    except Exception as e:
        print("No candidates inputted yet - Error type: ", e.__class__.__name__)

#turns the dict from GPT API to candidate profile.
def parse_dict_to_candidate(json): 
    candidate = Candidate(0, json["full_name"], json["experience"], json["studies"], json["contact"], json["misc"], json["analysis"], json["score"])
    candidates.append(candidate)
     # Sorts candidates by best score
    candidates.sort(key=lambda x: x.score)

#returns API response: helper function with request to GPT's API
def get_completion(messages, temperature=0, max_completion_tokens=None):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=temperature,
        max_completion_tokens=max_completion_tokens
    )
    return response.choices[0].message.content

#returns API response: concatanates model messages and calls helper function
def prompt_gpt(user_message, system_message):
    user_message= user_message
    system_message = system_message
    messages = [  
        {'role':'system', 'content': system_message},    
        {'role':'user', 'content': f"{DELIMITER}{user_message}{DELIMITER}"},  
    ] 
    return get_completion(messages)

#returns CV text from PDF
def extract_text(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

#reads .txt files - as an f string
def read_txt_file(text_file, *args):
    str = open(text_file, "r").read()
    return eval(f'{str}')


if __name__ == "__main__":
    main()