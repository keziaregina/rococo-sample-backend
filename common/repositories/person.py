import datetime
from uuid import UUID
from common.repositories.base import BaseRepository
from common.models.person import Person
from rococo.models.versioned_model import VersionedModel
from app.helpers.response import get_success_response, get_failure_response, parse_request_body, validate_required_fields

from common.app_logger import logger


class PersonRepository(BaseRepository):
    MODEL = Person

    def create_person(self, person: Person):
        new_person = Person(
            first_name = person.first_name,
            last_name = person.last_name,
        )
        try:
            self.save(new_person)
            return new_person 
        except Exception as e:
            logger.error(f"Failed to create person: {str(e)}")
            raise

    def update_person(self, person: VersionedModel):
        person.first_name = person.first_name
        person.last_name = person.last_name
        try:
            self.save(person)
            return person
        except Exception as e:
            logger.error(f"Failed to update person: {str(e)}")
            raise

    def get_person_by_id(self, entity_id: str):
        try:
            person = self.get_one({"entity_id": entity_id})
            return person
        except Exception as e:
            logger.error(f"Failed to get person by id: {str(e)}")
            raise

    def get_all_persons(self):
        try:
            persons = self.get_many()
            return persons
        except Exception as e:
            logger.error(f"Failed to get all persons: {str(e)}")
            raise

    def delete_person_by_id(self, person: Person):
        try:
            self.delete(person)
            return person
        except Exception as e:
            logger.error(f"Failed to delete person by id: {str(e)}")
            raise