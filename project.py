import os
import openai
import pdfplumber
import ast
import pickle
import json
from collections import defaultdict
from Candidate import Candidate
from dotenv import load_dotenv

load_dotenv()

SYSTEM_MESSAGE_TEXT_FILE = "system_message.txt"
JOB_DETAILS_TEXT_FILE = "job_details.txt"
DELIMITER = "####"
CV_FOLDER_PATH = "./CV"

#depending on input of user



#list of Candidate objects
candidates = []

def main():
    
    chatgpt_setup()

    load_candidates()
    for file in os.listdir(cv_folder_path):

        pdf_path = cv_folder_path + "/" + file
        if file == ".DS_Store" or file_analyzed(file):
            continue

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

        # add a value to the candidate object
        output_dict["file_name"] = file

        # turns the dict with relevant information about the candidate to an instance of the Candidate object.
        parse_dict_to_candidate(output_dict)
        #preview.

    store_candidates_json(candidates)

def chatgpt_setup():

    openai.api_key = os.environ['OPENAI_API_KEY']

    # Declare global client
    global client
    client = openai.OpenAI()

def file_analyzed(file):
    for candidate in candidates:
        if file == candidate.file_name:
            return True
    return False

def store_candidates_json(candidates):

    candidates_json = []

    with open("candidates_json.json", "w") as file:
        
        for candidate in candidates:

            candidates_json.append({
                "full_name":candidate.full_name,
                "file_name":candidate.file_name,
                "experience":candidate.experience,
                "studies":candidate.studies,
                "contact":candidate.contact,
                "misc":candidate.misc,
                "analysis":candidate.analysis,
                "score":candidate.score,
            })
        json.dump(candidates_json, file, indent=4)

        json.dump(candidates_json, file, indent=4)

def load_candidates_json():
    #load to a list after instanciating them.
    try:
        with open("candidates_json.json", "r") as file:
            list = json.load(file)
            for candidate in list:
                candidates.append(create_candidate(candidate))
    except FileNotFoundError:
        print("No such file to load.")


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
    
    with pdfplumber.open(pdf_path) as pdf:

        return ' '.join([page.extract_text() for page in pdf.pages])
    
#reads .txt files - as an f string
def read_txt_file(text_file, *args):
    str = open(text_file, "r").read()
    return eval(f'{str}')


if __name__ == "__main__":
    main()