from __future__ import annotations
from dataclasses import dataclass, field

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.dog import Dog

@dataclass
class Owner:
    id: int
    phone_number: str
    phone_name: str
    first_name: str
    last_name: str
    note: str
    dogs: list[Dog] = field(repr=False)
