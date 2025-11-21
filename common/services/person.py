from common.repositories.factory import RepositoryFactory, RepoType
from common.models.person import Person


class PersonService:

    def __init__(self, config):
        self.config = config

        from common.services import EmailService
        self.email_service = EmailService(config)

        self.repository_factory = RepositoryFactory(config)
        self.person_repo = self.repository_factory.get_repository(RepoType.PERSON)

    def save_person(self, person: Person):
        person = self.person_repo.save(person)
        return person

    def get_person_by_email_address(self, email_address: str):
        email_obj = self.email_service.get_email_by_email_address(email_address)
        if not email_obj:
            return
        
        person = self.person_repo.get_one({"entity_id": email_obj.person_id})
        return person

    def get_person_by_id(self, entity_id: str):
        person = self.person_repo.get_one({"entity_id": entity_id})
        return person

    def get_all_persons(self):
        persons = self.person_repo.get_many()
        return persons

    def update_person(self, person: Person):
        person = self.person_repo.update_person(person)
        return person

    def delete_person(self, person: Person):
        print (person.as_dict())
        person = self.person_repo.delete(person)
        return person

    def create_person(self, first_name: str, last_name: str):
        person = Person(
            first_name=first_name,
            last_name=last_name
        )
        person = self.person_repo.add_person(person)
        return person