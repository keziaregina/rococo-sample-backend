import datetime
from uuid import UUID
from common.repositories.base import BaseRepository
from common.models.person import Person
from rococo.models.versioned_model import VersionedModel
from app.helpers.response import get_success_response, get_failure_response, parse_request_body, validate_required_fields


class PersonRepository(BaseRepository):
    MODEL = Person

    def create_person(self, person: Person):
        new_person = Person(
            first_name = person.first_name,
            last_name = person.last_name,
        )
        self.save(new_person)
        return new_person

    def update_person(self, person: VersionedModel):
        person.first_name = person.first_name
        person.last_name = person.last_name
        self.save(person)
        return person

    def get_person_by_id(self, entity_id: str):
        person = self.get_one({"entity_id": entity_id})
        return person

    def get_all_persons(self):
        persons = self.get_many()
        return persons

    def delete_person_by_id(self, person: Person):
        self.delete(person)
        return person