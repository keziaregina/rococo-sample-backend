from typing import ClassVar
from dataclasses import dataclass, field
# from . import VersionedModel
from rococo.models.versioned_model import VersionedModel


@dataclass
class Task(VersionedModel):
    use_type_checking: ClassVar[bool] = True

    person_id: str = None
    title: str = None
    description: str = None
    is_complete: bool = False