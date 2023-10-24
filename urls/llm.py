import json
import os
from flask import Blueprint, request
from flask_cors import cross_origin
from dotenv import load_dotenv

# Import langchain library and dependencies
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain.chains import ConversationChain

# Define blueprint
llm_bp = Blueprint('/llm', __name__)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Init langchain OpenAI module
llm = OpenAI(temperature=0.9)

# Init ConversationChain
# ConversationChain holds historical communication with AI
convo = ConversationChain(llm=OpenAI(temperature=0.7))

# Standard Prompt Templates for reusability with minimum input from the user
common_diseases_per_country = PromptTemplate(
    input_variables =['country'],
    template = "what is the most common diseases in {country}? Respond with just the disease name."
)

most_common_diseases_chain =LLMChain(llm=llm, prompt=common_diseases_per_country, output_key="disease_name")

common_symptoms_prompt = PromptTemplate(
    input_variables = ['disease_name'],
    template="What are the most common symptoms of {disease_name} for each disease mentioned by the first prompt? Answer as a list of strings."
)

common_symptoms_chain =LLMChain(llm=llm, prompt=common_symptoms_prompt, output_key="symptoms")

# Sequential Chain takes response from first in the chain and passes the value on to the next chain
# Order of the chain in the list is important
chain = SequentialChain(
    chains = [most_common_diseases_chain, common_symptoms_chain],
    input_variables = ['country'],
    output_variables = ['disease_name', "symptoms"]
)

# Single Query predicts answer to an input, without holding on to the previous inputs in the memory
@llm_bp.route("/single-query", methods=["POST"])
@cross_origin()
def single_query():
    question = json.loads(request.data).get("question")
    if not question:
        return {"success": False, "data": "missing_parameters: question"}    
    llm_response = llm.predict(question)
    return {"success": True, "data": llm_response}

# Get Previous Conversation from memory buffer
@llm_bp.route("/convo-chain", methods=["GET"])
@cross_origin()
def get_convo_chain():
    llm_response = convo.memory.buffer
    return {"success": True, "data": llm_response}

# Send input to a conversation Chain
@llm_bp.route("/convo-chain", methods=["POST"])
@cross_origin()
def convo_chain():
    question = json.loads(request.data).get("question")
    if not question:
        return {"success": False, "data": "missing_parameters: question"}    
    llm_response = convo.run(question)
    return {"success": True, "data": llm_response}


@llm_bp.route("/most-common-disease-per-country")
@cross_origin()
def most_common_disease_per_country():
    country = request.args.get("country")
    if not country:
        return {"success": False, "data": "missing_parameters: country"}    
    chain_response = most_common_diseases_chain.run(country)
    return {"success": True, "data": chain_response}


@llm_bp.route("/chain-country-disease-symptoms")
@cross_origin()
def chain_country_disease_symptoms():
    chain_response = chain("India")
    return {"success": True, "data": chain_response}
