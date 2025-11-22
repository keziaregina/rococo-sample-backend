import datetime
from uuid import UUID
from common.app_logger import logger
from common.repositories.base import BaseRepository
from common.models.task import Task


class TaskRepository(BaseRepository):
    MODEL = Task

    def create_task(self, task: Task):
        try:
            self.save(task)
            return task
        except Exception as e:
            logger.error(f"Failed to create task: {str(e)}")
            raise

    def get_task_by_id(self, entity_id: str):
        try:
            task = self.get_one({"entity_id": entity_id})
            return task
        except Exception as e:
            logger.error(f"Failed to get task by id: {str(e)}")
            raise

    def get_tasks_by_person_id(self, person_id: int, is_complete: bool = None):
        if is_complete is None:
            return self.get_many({"person_id": person_id})
        else:
            is_complete = is_complete.title()
            return self.get_many({"person_id": person_id, "is_complete": is_complete})

    def update_task(self, task: Task):
        task.title = task.title
        task.description = task.description

        try:
            self.save(task)
            return task
        except Exception as e:
            logger.error(f"Failed to update task: {str(e)}")
            raise

    def delete_task(self, task: Task):
        try:
            self.delete(task)
            return task
        except Exception as e:
            logger.error(f"Failed to delete task: {str(e)}")
            raise

    def mark_as_complete(self, task: Task):
        task.is_complete = True
        try:
            self.save(task)
            return task
        except Exception as e:
            logger.error(f"Failed to mark as complete: {str(e)}")
            raise

    def mark_as_incomplete(self, task: Task):
        task.is_complete = False
        try:
            self.save(task)
            return task
        except Exception as e:
            logger.error(f"Failed to mark as incomplete: {str(e)}")
            raise