"""Helper functions"""

import os
import json
from typing import AsyncGenerator

from loguru import logger
from aiohttp import ClientSession
import aiofiles
from asyncache import cached as acached
from cachetools import TTLCache

cache_timer = int(os.getenv("CACHE_TIMER", 300))
ROOT_URL = "http://sia/v1/run"

DATA_BLOB_BASE_URI = "http://data-blob/v1"
DATA_BLOB_TABLE_ENDPOINT = f"{DATA_BLOB_BASE_URI}/table" + "/{table_name}"

DATA_GRAPH_BASE_URI = "http://data-graph/v1"
DATA_GRAPH_RUN_ENDPOINT = f"{DATA_GRAPH_BASE_URI}/run"
DATA_GRAPH_RUNDSCRIPT_ENDPOINT = f"{DATA_GRAPH_RUN_ENDPOINT}" + "/{graph_script_name}"
DATA_GRAPH_GROUP_MEMBERSHIP_ENDPOINT = f"{DATA_GRAPH_BASE_URI}/groupMembership"

def format_elapsed_time(total_seconds) -> str:
    """Formats a timedelta object to a human readable string.
    
    Args:
        total_seconds (int): The total number of seconds.
    
    Returns:
        str: The formatted elapsed time string.
        
    """
    if total_seconds < 60:
        return f"{total_seconds}sec"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02}min"
    else:
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours}:{minutes:02}h"
    
@acached(cache=TTLCache(maxsize=32, ttl=cache_timer))
async def read_json(path: str) -> dict:
    """Reads a JSON file and returns its content as a dictionary.
    
    Args:
        path (str): The path to the JSON file.
        
    Returns:
        dict: The content of the JSON file as a 
        dictionary.

    Raises:
        FileNotFoundError: If the specified file
        does not exist.
        JSONDecodeError: If the file content is
        not valid JSON.
    """

    async with aiofiles.open(path) as file:
        content = await file.read()
        data =  json.loads(content)
    return data

async def stream_ndjson(response) -> AsyncGenerator[dict: None]:
    """Stream and process NDJSON data from the response.
    
    Args:
        response: The response object containing the NDJSON data.
    
    Yields:
        A dictionary representing each line of the NDJSON data.
        
    """
    buffer = ""
    async for chunk in response.content.iter_any():
        buffer += chunk.decode("utf-8")
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            if line:
                yield json.loads(line)

async def call_api(url: str, headers: dict | None = None, timeout: int = 100, method: str = "POST", **kwargs):
    """Calls the graph API with the specified URL, headers, body, timeout, and session."""
    headers = headers or {}

    logger.info(f"Calling API: {url}")
    async with ClientSession(trust_env=True) as session:
        if method == "POST":
            async with session.post(url=url, timneout=timeout, headers=headers, **kwargs) as response:
                logger.info("Run POST")
                if response.status == 401:
                    text = await response.text()
                    logger.error(f"Error calling graph: {text}")
                    raise ValueError("Failed to authenticate on API.")
                response.raise_for_status()
                data = await response.json()
                return data
        elif method == "GET":
            logger.info("Run GET")
            async with session.get(url=url, timeout=timeout, headers=headers, **kwargs) as response:
                if response.status == 401:
                    text = await response.text()
                    logger.error(f"Error calling graph: {text}")
                    raise ValueError("Failed to authenticate on API.")
                response.raise_for_status()
                data = await response.json()
                return data
        else:
            raise ValueError("Invalid method provided.")