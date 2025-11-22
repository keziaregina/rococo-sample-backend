from common.repositories.base import BaseRepository
from common.models.login_method import LoginMethod
from common.app_logger import logger


class LoginMethodRepository(BaseRepository):
    MODEL = LoginMethod

    def create_login_method(self, login_method: LoginMethod):
        login_method.person_id = login_method.person_id
        login_method.email_id = login_method.email_id
        try:
            self.save(login_method)
            return login_method
        except Exception as e:
            logger.error(f"Error creating login method: {e}")
            raise e

    def get_login_method_by_email_id(self, email_id: str):
        try:
            login_method = self.get_one({"email_id": email_id})
            return login_method
        except Exception as e:
            logger.error(f"Error getting login method by email id: {e}")
            raise e