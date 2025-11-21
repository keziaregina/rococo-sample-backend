from rococo.models import Person as BasePerson
from typing import ClassVar


class Person(BasePerson):
    use_type_checking: ClassVar[bool] = True

    first_name: str = None
    last_name: str = None