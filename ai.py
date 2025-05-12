from openai import OpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

class Job(BaseModel):
    title: str
    salary: str
    company: str
    city: str
    url: str
    description: str

class JobList(BaseModel):
    jobs: list[Job]



