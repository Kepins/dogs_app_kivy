from __future__ import annotations
from dataclasses import dataclass, field

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.owner import Owner
    from entities.appointment import Appointment
    from entities.breed import Breed
    from entities.size import Size


@dataclass
class Dog:
    id: int
    name: str
    owner: Owner
    breed: Breed
    size: Size
    note: str
