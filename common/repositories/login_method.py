from common.repositories.base import BaseRepository
from common.models.login_method import LoginMethod


class LoginMethodRepository(BaseRepository):
    MODEL = LoginMethod

    def create_login_method(self, login_method: LoginMethod):
        login_method.person_id = login_method.person_id
        login_method.email_id = login_method.email_id
        self.save(login_method)
        return login_method

    def get_login_method_by_email_id(self, email_id: str):
        login_method = self.get_one({"email_id": email_id})
        return login_method