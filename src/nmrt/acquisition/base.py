from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class AcquisitionChannel:
    physical_id: str
    name: str
    unit: str = "V"
    signal_type: str = "generic"
    scale: float = 1.0
    offset: float = 0.0


class AcquisitionAdapter(ABC):
    """Contract for optional live hardware backends.

    Vendor SDKs/drivers should remain optional dependencies and should not leak into the scientific core.
    """

    @abstractmethod
    def discover(self) -> list[str]: ...

    @abstractmethod
    def configure(self, *, sample_rate: float, channels: list[AcquisitionChannel]) -> None: ...

    @abstractmethod
    def start(self, on_chunk: Callable[[np.ndarray, float], None]) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...
