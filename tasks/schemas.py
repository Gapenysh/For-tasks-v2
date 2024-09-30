from __future__ import annotations

import datetime
from typing import Annotated, Optional
from annotated_types import MaxLen, MinLen

from pydantic import BaseModel, ConfigDict


class Task(BaseModel):
    title: Annotated[str, MinLen(5), MaxLen(600)]
    detail: Optional[str]
    creation_date: datetime.date
    execution_date: datetime.date
    execution_mark: Annotated[str, MinLen(6), MaxLen(10)]
    executors: list[int]


class TaskUpdate(BaseModel):
    title: Optional[Annotated[str, MinLen(5), MaxLen(600)]]
    detail: Optional[str]
    creation_date: Optional[datetime.date]
    execution_date: Optional[datetime.date]
    execution_mark: Optional[Annotated[str, MinLen(6), MaxLen(10)]]


class TaskStatusUpdate(BaseModel):
    status: Optional[Annotated[str, MinLen(6), MaxLen(10)]]
