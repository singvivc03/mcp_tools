from mcp.server.fastmcp import FastMCP
from openai import OpenAI
import tempfile
from dotenv import load_dotenv
import os

from openai.types import VectorStore

## Load environment file from .env if present
load_dotenv(verbose=True)

client = OpenAI()
VECTOR_STORE_NAME = "MEMORIES"

mcp = FastMCP("Memories")

def get_or_create_vector_store() -> VectorStore:
     """Try to find existing vector store or create"""
     stores = client.vector_stores.list()
     for store in stores:
         if store.name == VECTOR_STORE_NAME:
             return store
     return client.vector_stores.create(name=VECTOR_STORE_NAME)

@mcp.tool()
def save_memory(memory: str) -> dict[str, str]:
    """Save a memory string to the vector store"""
    vector_store = get_or_create_vector_store()
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as f:
        f.write(memory)
        f.flush()
        client.vector_stores.files.upload_and_poll(vector_store_id=vector_store.id, file=open(f.name, "rb"))
    return {"status": "success", "vector_store_id": vector_store.id}

@mcp.tool()
def search_memory(query: str) -> dict[str, list[str]]:
    """Search memories in the vector store and return relevant content"""
    vector_store = get_or_create_vector_store()
    results = client.vector_stores.search(vector_store_id=vector_store.id, query=query)
    content_text = [
        content.text
        for item in results.data
        for content in item.content
        if content.type == 'text'
    ]
    return {"results": content_text}

if __name__ == "__main__":
    mcp.run(transport="stdio")