import datetime
from uuid import UUID
from common.repositories.base import BaseRepository
from common.models.task import Task
from rococo.models.versioned_model import VersionedModel


class TaskRepository(BaseRepository):
    MODEL = Task

    def add_task(self, task: Task):
        new_task = Task(
            person_id=1,
            title = task.title,
            description = task.description,
            is_complete = False,
        )
        self.save(new_task)
        return new_task

    def get_tasks_by_person_id(self, person_id: int):
        query = """
            SELECT * FROM task WHERE person_id = %s;
        """
        params = (person_id)
        with self.adapter:
            results = self.adapter.execute_query(query, params)
            return results

    def update_task(self, task: Task):
        task.title = task.title
        task.description = task.description

        self.save(task)
        return task

    def mark_as_complete(self, task: Task):
        task.is_complete = True
        self.save(task)
        return task