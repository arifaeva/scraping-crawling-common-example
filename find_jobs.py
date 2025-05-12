import chromadb
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
import asyncio
import json

async def main():
    chroma = await chromadb.AsyncHttpClient("localhost", 8000)
    collection = await chroma.get_collection(
        name="job_list",
        embedding_function=ONNXMiniLM_L6_V2(),
    )

    queries = await collection.query(
        query_texts=["Administrator"],
        n_results=2,
        where={"city": "Surabaya, Jawa Timur"}
    )

    print(json.dumps(queries, indent=4))

if __name__ == "__main__":
    asyncio.run(main())