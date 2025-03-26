from agno.agent import Agent
from agno.models.groq import Groq
from textwrap import dedent
import os
from dotenv import load_dotenv
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.newspaper import NewspaperTools
from agno.storage.json import JsonStorage

from pdfReaderTool import PdfReaderTool  # Custom python function to read text data from PDF
from modelTool import RiskScorer
from jsonWriterTool import JSONWriterTool
from fastapi import FastAPI
from agno.tools.file import FileTools
from pathlib import Path
# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Instantiate PdfReaderTool
pdfData = PdfReaderTool()
txt = pdfData.run("txns.pdf") #For some reason agent is unable to call the function 

# Create the data analyst Agent for initial data analysis and extraction
dataAnalystAgent = Agent(
    name= "DataAnalystAgent",
    model=Groq(id="llama3-70b-8192"),
    description="You are an experienced data analyst expert in analyzing data and extracting required details from it.",
    instructions=dedent(f"""
            Follow these instructions to identify the transactions and extract the required data from the text:
            1) The data contains financial transaction or ownership information involving two or more entities.
               The entities can be names of organizations or persons and play roles like beneficial owners, directors, etc.
            2) The data can have transactions listed both in structured and unstructured format.
            3) Extract the transaction ID, payer name, receiver name, related entities, and transaction amounts.
               If there is no transaction amount, consider it as 0, but extract the associated entities based on ownership, roles, etc.
            4) The structured text will have entities labeled with headers such as:
               'Payer Name', 'Receiver Name', 'Amount', 'Transaction Details', 'Receiver Country', 
               and a unique identifier for the transaction ID that begins with 'TXN'.
            5) If the Transaction ID is not mentioned, assign a unique dummy value starting with 'NTX'.
            Each transaction should have these attributes: Transaction Id, Extracted Entity as an array, transaction amount, countries.
                                 
            The given data is as follows : {txt}                        

    """),
    expected_output=dedent(f"""
       Output the extracted content as json with the following attributes for each transaction - Transaction ID , Entity, Transaction Amount and Countries.
    """),
    show_tool_calls=True,
    markdown=True,
)


researchAnalystAgent = Agent(
    name="ResearchAnalystAgent",
    model=Groq(id="deepseek-r1-distill-llama-70b"),
    description="You are an expert research analyst and can research about entities on the internet",
    instructions=dedent(f"""
                        For a given list of entities, search the internet for news articles and public respositories in the following way -
                        1) The websites you can use to get this data are below using the DuckDuckgo tool - 
                           OpenCorporates, Wikidata, OFAC Sanctions List, SEC EDGAR. 
                        2) Also look up news articles using Newspaper tool for these entities and stop after getting top 5 results.
                        3) After getting the results, classify each entity strictly as one of the following - Corporation, Shell Company, NGO, PEP, Individual. 
                        4) Also capture the source of information -website for this classification as supporting evidence.
                        5) Output the data in a JSON format mentioning the entity Name ,classification and supporting evidence source for such classification.
    """),
    tools=[DuckDuckGoTools(fixed_max_results=5,news=5),NewspaperTools()],
    expected_output=dedent(f"""
       Output the data in a JSON format mentioning the Transaction ID, Entity Name ,classification and supporting evidence source for such classification.
    """),
    markdown=True,
    show_tool_calls=True,
)
riskModelTool = RiskScorer()
riskAnalystAgent = Agent(
    name="RiskAnalystAgent",
    model=Groq(id="llama-3.3-70b-versatile"),
    description="You are a risk analyst to predict risk scores for given entities based on transaction details, entity type classification, payment amount and country",
    instructions=dedent("""
                         You are expected to predict the risk scores for the given entities based on transaction details, entity type classification, payment amount and country
                         You should call the given risk model tool to accomplish this task by passing the transactionDetails parameter.
                         E.g. parameter would be given like below. 
                          transaction = {
                                             'Transaction Details': 'Invoice settlement',
                                             'Amount': '$322000',
                                             'Receiver Country': 'India',
                                             'Entity Type': 'Non-Profit'
                                          }
                          Do the same for all the given entities and get the corresponding risk score. 

    """),
    tools=[riskModelTool],
    expected_output=dedent(f"""
       Output the data in a JSON format mentioning the given Transaction IDs, Entity Names and corrsponding predicted risk scores.
    """),
    markdown=True,
    show_tool_calls=True,
)

jsonWriter = JSONWriterTool("finalOutput.json")
multi_ai_agent_team=Agent(
    name="EI_Team_Coordinator",
    team=[dataAnalystAgent,researchAnalystAgent,riskAnalystAgent],
    model=Groq(id="llama-3.3-70b-versatile"),   
    instructions=dedent(f"""
                        You are a team coordinator and responsible to get the tasks done in a sequential manner. 
                        1) First ask the data analyst to work on the task given to it.
                        2) With the entities list extracted by the data analyst pass the information to the research analyst to work on its task.
                        3) After the research analyst completes its task pass the information from both data analyst and research analyst to the 
                         risk analyst to predict risk scores for the extracted entities.
                        4) After the risk analysist is done with the task use the output returned by data analyst, research analyst and risk analyst combined 
                        to create the final JSON response by combining all of them which should have the following attributes - 
                        Transacton Id, Extracted Entity, Entity Type, Risk Score, Supporting Evidence, Confidence Score,Reason for every transaction. 
    """),
    tools = [FileTools(Path("out"))],
    expected_output=dedent(f"""
       Output the final response json to a file using the given tool and filename 'final_JSON.json'. The json should have following attributes - 
         Transacton Id, Extracted Entity, Entity Type, Risk Score, Supporting Evidence, Confidence Score,Reason for every transaction.
    """),
    show_tool_calls=True,
    markdown=True,
)


#Expose the agent Team as API 
app= FastAPI()

@app.get("/agent")
async def start():
    response = multi_ai_agent_team.run()
    return {"response": response.content}


# Print the response 
if __name__ == "__main__":
   multi_ai_agent_team.print_response()