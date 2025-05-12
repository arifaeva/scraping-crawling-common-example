import asyncio
from crawl4ai import AsyncWebCrawler
from ai import client, JobList, Job
import chromadb
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2

async def main():
    chroma = await chromadb.AsyncHttpClient("localhost", 8000)
    collection = await chroma.create_collection(
        name="jobs",
        embedding_function=ONNXMiniLM_L6_V2
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://id.jobstreet.com/id/jobs/in-Surabaya-Jawa-Timur")
        
        res = client.beta.chat.completions.parse(
            model="gpt-4.1",
            messages=[
                { "role": "system", "content": "Extract job list based on given text" },
                { "role": "user", "content": result.markdown },
            ],
            response_format=JobList
        )

        response = res.choices[0].message.parsed
        for job in response.jobs:
            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(job.url)

                res = client.beta.chat.completions.parse(
                    model="gpt-4.1",
                    messages=[
                        { "role": "system", "content": "Extract job list based on given text" },
                        { "role": "user", "content": result.markdown },
                    ],
                    response_format=Job,
                )

                job_data = res.choices[0].message.parsed

                collection.add(
                    documents=[str(job_data.model_dump())],
                    ids=[job_data.url],
                    metadatas=[
                        {
                            "source": "jobstreet",
                            "city": job.city,
                        }
                    ]
                )

if __name__ == "__main__":
    asyncio.run(main())

# import asyncio
# from crawl4ai import AsyncWebCrawler, BrowserConfig, ProxyConfig
# from ai import client, JobList, Job

# proxy_config = ProxyConfig(
#     server="",
#     username="",
#     password="",
# )

# config = BrowserConfig(proxy_config=proxy_config)

# async def main():
#     async with AsyncWebCrawler(config=config) as crawler:
#         result = await crawler.arun("https://id.jobstreet.com/id/jobs/in-Surabaya-Jawa-Timur")
        
#         res = client.beta.chat.completions.parse(
#             model="gpt-4.1",
#             messages=[
#                 { "role": "system", "content": "Extract job list based on given text" },
#                 { "role": "user", "content": result.markdown },
#             ],
#             response_format=JobList
#         )

#         response = res.choices[0].message.parsed
#         for job in response.jobs:
#             async with AsyncWebCrawler(config=config) as crawler:
#                 result = await crawler.arun(job.url)

#                 res = client.beta.chat.completions.parse(
#                     model="gpt-4.1",
#                     messages=[
#                         { "role": "system", "content": "Extract job list based on given text" },
#                         { "role": "user", "content": result.markdown },
#                     ],
#                     response_format=Job,
#                 )

#                 job_data = res.choices[0].message.parsed

#                 # Insert to database
#                 with open("jobs.log", "a") as f:
#                     f.write(f"{job_data.model_dump()}\n")

# if __name__ == "__main__":
#     asyncio.run(main())