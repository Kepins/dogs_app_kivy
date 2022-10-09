from __future__ import annotations
from dataclasses import dataclass, field

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.appointment import Appointment


@dataclass
class Service:
    id: int
    name: str
