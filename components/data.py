from datetime import UTC, datetime

from helper import write_log
from loguru import logger
import chainlit as cl
import chainlit.data as cl_data
from chainlit.core import BaseDataLayer
from chainlit.step import StepDict
from chainlit.types import Feedback, PageInfo, ThreadDict, PaginatedResponse

DEFAULT_THREADS = {}

class CustomDataLayer(BaseDataLayer):
    def __init__(self):
        self.feedbacks = []
        self.users = {"id": None}
        self.threads = DEFAULT_THREADS

    async def create_user(self, user: cl.User) -> None:
        self.users[user.identifier] = user

    async def get_user(self, identifier: str) -> cl.User | None:
        return self.users.get(identifier)
    
    async def create_feedback(self, feedback: cl_data.Feedback) -> None:
        logger.debug("FEEDBACK GIVEN")

        self.feedbacks.append(feedback)

    async def get_feedback(self, feedback_id: str) -> cl_data.Feedback | None:
        logger.debug("FEEDBACK RETRIEVED")

        for feedback in self.feedbacks:
            if feedback.id == feedback_id:
                return feedback
        return None
    
    async def upsert_feedback(self, feedback: Feedback) -> str:
        logger.debug("FEEDBACK UPDATED")

        payload = {"PartitionKey": "user", "RowKey": self.id, "Feedback": feedback.value, "Comment": feedback.comment}
        await write_log(table="SessionLog", body=payload)

        return ""
    
    async def list_feedbacks(self) -> dict[str, cl_data.Feedback]:
        logger.debug("FEEDBACKS LISTED")

        return {feedback.id: feedback for feedback in self.feedbacks}
    
    async def get_thread_author(self, thread_id: str):
        logger.debug("GET THREAD AUTHOR CALLED")
        logger.trace(self.threads.get(thread_id, {}))

        return self.threads.get(thread_id, {}).get("threadId")
    
    async def get_thread(self, thread_id: str) -> ThreadDict | None:
        logger.debug("GET THREAD CALLED")
        logger.trace(thread_id)

        return self.threads.get(thread_id)
    
    async def list_threads(self, pagination: cl_data.Pagination, filters: cl_data.ThreadFilter) -> PaginatedResponse[ThreadDict]:
        logger.debug("LIST THREAD CALLED")
        logger.trace(f"{pagination=} {filters=}")

        threads_list = list(self.threads.values())
        info = PageInfo(hasNextPage=False, startCursor=None, endCursor=None)
        return cl_data.PaginatedResponse(data=threads_list, pageInfo=info)
    
    async def update_thread(self, thread_id: str, name: str = None, user_id: str = None, metadata: dict = None, tags: list[str] = None) -> None:
        logger.debug("UPDATE THREAD CALLED")
        logger.trace(f"{thread_id=} {name=} {user_id=} {metadata=} {tags=}")

        thread = self.threads.get(thread_id)

        if thread:
            thread["id"] = "hpdfl"
            if name:
                thread["name"] = name
            if user_id:
                thread["userId"] = user_id
            if metadata:
                thread["metadata"] = metadata
            if tags:
                thread["tags"] = tags
        else:
            self.threads[thread_id] = {
                "id": thread_id,
                "name": name,
                "metadata": metadata,
                "tags": tags,
                "createdAt": datetime.now(UTC).isoformat(),
                "userId": user_id,
                "steps": [],
            }

    async def delete_thread(self, thread_id: str) -> bool:
        logger.debug("DELETE THREAD CALLED")

        if thread_id in self.threads:
            del self.threads[thread_id]
            return True
        return False
    
    @cl_data.queue_until_user_message()
    async def create_step(self, step_dict: StepDict) -> None:
        logger.debug("CREATE STEP CALLED")
        logger.trace(step_dict)
        logger.trace(self.threads)

        thread_id = step_dict.get("threadId")
        thread = self.threads.get(thread_id)

        if thread:
            logger.trace(thread)
            step = {
                "id": step_dict.get("id"),
                "name": step_dict.get("name"),
                "createdAt": step_dict.get("createdAt"),
                "type": step_dict.get("type"),
                "output": step_dict.get("output"),
            }
            self.threads[thread_id]["steps"].append(step)
            logger.trace(self.threads[thread_id])
        else:
            await self.update_thread(
                thread_id,
                name="New Thread",
                user_id=step_dict.get("name"),
                metadata=step_dict.get("metadata", {}),
                tags=step_dict.get("metadata", []),
                
            )