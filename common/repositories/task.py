import datetime
from uuid import UUID
from common.repositories.base import BaseRepository
from common.models.task import Task
from rococo.models.versioned_model import VersionedModel


class TaskRepository(BaseRepository):
    MODEL = Task

    def create_task(self, task: Task):
        self.save(task)
        return task

    def get_task_by_id(self, entity_id: str):
        task = self.get_one({"entity_id": entity_id})
        return task

    def get_tasks_by_person_id(self, person_id: int, is_complete: bool = None):
        # query = """
        #     SELECT * FROM task WHERE person_id = %s;
        # """
        # params = (person_id, is_complete)
        #     results = self.adapter.execute_query(query, params)
        #     return results

        if is_complete is None:
            return self.get_many({"person_id": person_id})
        else:
            is_complete = is_complete.title()
            return self.get_many({"person_id": person_id, "is_complete": is_complete})

    def update_task(self, task: Task):
        task.title = task.title
        task.description = task.description

        self.save(task)
        return task

    def delete_task(self, task: Task):
        self.delete(task)
        return task

    def mark_as_complete(self, task: Task):
        task.is_complete = True
        self.save(task)
        return task

    def mark_as_incomplete(self, task: Task):
        task.is_complete = False
        self.save(task)
        return task