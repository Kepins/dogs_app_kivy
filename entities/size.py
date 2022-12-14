from __future__ import annotations
from dataclasses import dataclass, field

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.dog import Dog


@dataclass
class Size:
    id: int
    name: str
    dogs: list[Dog] = field(repr=False)
