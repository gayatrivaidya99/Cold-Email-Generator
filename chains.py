import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
# print("✅ langchain_groq is working!")


load_dotenv()   #find the .env file -> set it as env variable
# os.getenv("GROQ_API_KEY")

class Chain:

    def __init__(self):
        self.llm = llm = ChatGroq(
    model ="llama-3.3-70b-versatile",
    groq_api_key="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",
    temperature=0)
        

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
    """
    ### SCRAPED TEXT FROM WEBSITE:
    {page_data}
    ### INSTRUCTION:
    The scraped text is from the career's page of a website.
    Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills`, and `description`.
    Only return the valid JSON.
    ### VALID JSON (NO PREAMBLE):
    """
)
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})

        try:
            json_parser = JsonOutputParser()
            parsed = json_parser.parse(res.content)
            if isinstance(parsed, dict):
                return [parsed]  # wrap single dict in list
            elif isinstance(parsed, list):
                return parsed
            else:
                return []
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
You are a recent computer science graduate with a strong background in AI and software development. You have completed multiple academic and personal projects that demonstrate your technical and problem-solving abilities in areas such as machine learning, data pipelines, and full-stack development.

Your job is to write a personalized cold email to the hiring manager regarding the job mentioned above, expressing your interest and highlighting how your technical background and experience make you a strong fit for the role.

Also add the most relevant ones from the following links to showcase your project portfolio: {link_list}

Keep the email concise, professional, and enthusiastic. Do not include a preamble or explanation — just output the email directly.

### EMAIL (NO PREAMBLE):
"""
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content
    
    
if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))