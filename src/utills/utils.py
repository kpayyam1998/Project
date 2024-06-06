import os
import sys
import json
import openai
import re

from dotenv import load_dotenv
from spellchecker import SpellChecker
from src.exception import CustomException
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")  # Replace with your actual OpenAI API Key

key=os.getenv("OPENAI_API_KEY")
model=OpenAI(api_key=key)

# load data
def load_data(path):
    try:
        file_path = path 
        # Open the file in read mode
        with open(file_path, 'r') as file:
            company_data = json.load(file)       # Load the JSON data from the file

        return company_data
    except Exception as e:
        raise CustomException(e,sys)


# separate each page
def company_info(company_data):
    try:

        if not company_data:
            raise CustomException("Company data is not available")
        
        home=dict(company_data['pages'][0])
        about=dict(company_data['pages'][1])
        publications=dict(company_data['pages'][2])
        contacts=dict(company_data['pages'][3])

        company_about = {
        "businessName": company_data["businessName"],
        "Country": company_data["Country"],
        "product_type": company_data["product_type"],
        "business_info": company_data["business_info"]
        }
        
        final_data=[home,about,publications,contacts]


        return final_data,company_about
    except Exception as e:
        raise FileNotFoundError(e,sys)


# convert json string to json 
def load_json(data):
    return json.loads(data)

# using GPT llm
def llm(prompt):
   try:
      response = openai.Completion.create(
                  engine="gpt-3.5-turbo-instruct",
                  prompt=f"generate new content based on the prompt {prompt}",
                  max_tokens=1000,
                  temperature=0.7,
                  top_p=0.9,
                  frequency_penalty=0.5,
                  presence_penalty=0.5
                  ) 
      response=response.choices[0].text.strip()
      generate_data=load_json(response)
      return generate_data
   except Exception as e:
      raise CustomException(e,sys)
   
      

# Using Langchain
def prompt_template(page_data,template_format):
    try:
        prompt = PromptTemplate(
        input_variables=["template_format"],
        template=f""" Provide the content with format of json data{template_format}.Content should be unique very informative & US standards. 
                  should not use repeated words  """)
        chain = LLMChain(prompt=prompt, llm=model)

        result = chain.run(page_data=page_data,template_format=template_format)
        

        return result
    except Exception as e:
        raise CustomException(e,sys)
    
  

# generate conten
def generate_page_content(page_data, business_data):
 
  try:
      page_content = {}
      if page_data["page_type"] == "edit" and page_data["copyService"] == "newCopy":
        
        if page_data['title'] == "Home":
              
              prompt=f"""
                #Note: Dont provide html tags in the content section
                {page_data}
                # Based on the above data make content unique content and dont use repeated tags and words
                Provoide the content with json data.Content should be unique and crisp and attractive.
                if customerAction is not avaible then create unique customerAction fill that. 
                sample format data same thing you have to generate
                meta_title : Provoide unique title less than 30 words {page_data['seo_keywords']} - {business_data['businessName']}
                meta_description : Provoide description about more unique attractive  (70 to 143 Characters) {business_data['businessName']} insights with {business_data['businessName']}, US. Embark on your {page_data['seo_keywords']} journey today.
                Explore Publications.
                hero_title : provoide unique title based on the keyword title should (20 to 70 Characters)
                hero_text :Generate Unique content based onthe input keywords  
                CTA Button: Get In Touch (Button to Contact Page)
                h1_title: Unique  Enhancing title with (40 to 60 Characters) based on the  {page_data['seo_keywords']} in the US
                h1_content: Use above input content to make the new brief description about the content make more attractive (70 to 143 Characters 
                h2_title : Explore Case Studies
                h2_content:  Generate attractive content with using input {page_data['content']} with more than  words
                leading_sentence: Generate .
                
                
                ###########################################
                Json format output


              """
        
              generate_data=llm(prompt)
              print(generate_data)
              page_content["meta_title"] = f"{generate_data['meta_title']}"
              page_content["meta_description"] = f"{generate_data['meta_description']}"
              page_content["hero_title"] = f"{generate_data['hero_title']}"
              page_content["hero_text"] = f" {generate_data['hero_text']}"
              if page_data["notes"]!="":
                  page_content["notes"]=page_data["notes"]
              # if page_data['customerAction']=="":
              #    page_content["customerAction"] ="readMore"
              # page_content["customerAction"] =f"{page_data['customerAction']}"
                      
              page_content["h1"] = f"{generate_data['h1_title']} "
              page_content["h1_content"] = f"{generate_data['h1_content']}"
              page_content["h2"] = f"{generate_data['h2_title']}"
              page_content["h2_content"] =f"{generate_data['h2_content']}"
              page_content["leading_sentence"] = f"{generate_data['leading_sentence']}"           

        elif page_data['title'] == "About":
            
            template_format="""
                {page_data}
                Content ,Title should not be same 
                ##########################
                resonse json
                ##########################
                meta_title: select company name from input - provoide suitable title (specific field serivices) based on input
                meta_description: journey of the person and mention  company name where he worked. provide services based on the input(70-150) words)
                h1_title: Title should be unique and intract when the user see (10-40 words)
                h1_content: Suitable content based on the above input(90-150 words)
                h2_title:  Title should be unique and intract when the user see (Explore case studies)based on the above input (10-40 words)
                h2_content: Suitable content based on the above input and Explore case studies (90-100 words)
                leading_sentence: Based on the content provide leading_sentence upto 35 words
                """
                
            generate_data=prompt_template(page_data, template_format)
            
            data=load_json(generate_data)
            
            return data
            #return generate_data
            #print(type(generate_data))

      elif page_data["page_type"] == "view" and page_data["copyService"] == "":
        page_content = {
          "content": page_data["content"]
        }

      return page_content

  except Exception as e:
      raise CustomException(e,sys)

# Bullet check
def check_bullet_list(content):
    # Extract bullet list items
    bullet_list_items = re.findall(r"(^\s*[\*\-\+]\s+.*(?:(?:\n(?![\*\-\+]))+|(?:\s*\n\s*)*)$)", content, re.MULTILINE)

    # Check for supporting sentence or H2
    if not any(re.search(r"^\W*\w+", item) for item in bullet_list_items):
        return False

    # Check for punctuation in one-worded bullet lists
    for item in bullet_list_items:
        if len(item.split()) == 1 and not re.search(r"[.,!?]$", item):
            return False
        if len(item.split()) == 1 and re.search(r"[.,!?]$", item):
            if item != item.title():
                return False

    # Check for punctuation in sentences
    for item in bullet_list_items:
        if len(item.split()) > 1 and not re.search(r"[.,!?]$", item):
            return False

    # Check for periods in locations
    for item in bullet_list_items:
        if re.search(r"[A-Z]\s*to\s*[A-Z]", item) and "." in item:
            return False

    return True
  

# Spell checking
def spell_check(content):
    # pip install pyspellchecker
    spell = SpellChecker()

    # Find misspelled words
    misspelled = spell.unknown(content.split())

    corrections = {}
    for word in misspelled:
        # Get the one `most likely` answer
        corrections[word] = spell.correction(word)
        
    return corrections

   
# Business info contact  information
def parse_business_info(info):
    lines = info.strip().split('\n')  # Split business info details into lines
    info_dict = {}
    
    for line in lines:
        parts = line.split(':', 1)  # Split keys and values by the first colon
        if len(parts) == 2:
            key, value = parts
            info_dict[key.strip()] = value.strip()  # Store key and value in dictionary

    return info_dict