import asyncio
from crawl4ai import AsyncWebCrawler
from ai import client, JobList, Job
import chromadb
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2

async def main():
    chroma = await chromadb.AsyncHttpClient("localhost", 8000)
    collection = await chroma.create_collection(
        name="job_list",
        embedding_function=ONNXMiniLM_L6_V2()
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
        for job in response.jobs[:5]:
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

                # Validate (apakah ada yang sama atau tidak)

                # Insert to Django DB
                # Insert to Vector DB
                await collection.add(
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