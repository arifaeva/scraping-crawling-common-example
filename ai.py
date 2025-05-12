from openai import OpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

class Job(BaseModel):
    title: str
    category: str
    """Category: example -> 'IT', 'Sales'"""
    salary: str
    company: str
    city: str
    """City: example -> 'Surabaya', 'Jakarta'"""
    url: str
    description: str

class JobList(BaseModel):
    jobs: list[Job]