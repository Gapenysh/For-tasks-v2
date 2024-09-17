from typing import Annotated
from annotated_types import MaxLen, MinLen

from pydantic import BaseModel


class User(BaseModel):
    username: Annotated[str, MinLen(5), MaxLen(50)]
