from pydantic import BaseModel
from datetime import datetime
from typing import Union

class Worker(BaseModel):
    username: str

class Resume(BaseModel):
    title: str
    compensation: Union[int, None]
    worker_id: int
    create_at: Union[datetime, None]