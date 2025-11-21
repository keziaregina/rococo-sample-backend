import datetime
from uuid import UUID
from common.repositories.base import BaseRepository
from common.models.person import Person
from rococo.models.versioned_model import VersionedModel


class PersonRepository(BaseRepository):
    MODEL = Person

    def update_person(self, person: VersionedModel):
        new_person = Person(
            first_name = person.first_name,
            last_name = person.last_name,
        )
        new_person.first_name = 'new_person.first_name'
        new_person.last_name = 'new_person.last_name'
        person.prepare_for_save(changed_by_id=1) # todo: Change to the actual user id
        self.save(new_person)

    def add_person(self, person: Person):
        new_person = Person(
            first_name=person.first_name,
            last_name=person.last_name,
        )
        new_person.prepare_for_save(changed_by_id=1) # todo: Change to the actual user id
        self.save(new_person)
        return new_person

