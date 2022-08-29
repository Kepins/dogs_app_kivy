from __future__ import annotations
from dataclasses import dataclass

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.dog import Dog
    from entities.service import Service

    from datetime import datetime
    from decimal import *

@dataclass
class Appointment:
    id: int
    dog: Dog
    service: Service
    date: datetime
    cost: Decimal
