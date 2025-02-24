from loguru import logger

from .utils import DATA_BLOB_TABLE_ENDPOINT, call_api


async def write_log(table: str, body: dict):
    """Writes the session log entry to the data table."""
    try:
        await call_api(url=DATA_BLOB_TABLE_ENDPOINT.format(table_name=table), json=body)
        return True
    except Exception as e:
        logger.exception(f"Failed to write log message: {e}")
        if __debug__ is True:
            raise
        return False
    
async def get_log(table: str, params: dict):
    """Writes a log message to the specified table."""
    try:
        return await call_api(method="GET", url=DATA_BLOB_TABLE_ENDPOINT.format(table_name=table), params=params)
    except Exception as e:  #pylint: disable=W0703 # As here we really dont want anything to cause a failure in prod
        logger.exception(f"Failed to write log message: {e}")
        if __debug__ is True:
            raise