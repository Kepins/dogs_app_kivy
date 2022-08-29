from __future__ import annotations
from dataclasses import dataclass

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.dog import Dog

@dataclass
class Owner:
    id: int
    first_name: str
    last_name: str
    note: str
    dogs: [Dog]
