from common.repositories.factory import RepositoryFactory, RepoType
from common.models.task import Task


class TaskService:

    def __init__(self, config):
        self.config = config
        self.repository_factory = RepositoryFactory(config)
        self.task_repo = self.repository_factory.get_repository(RepoType.TASK)

    def get_task_by_id(self, entity_id: str):
        task = self.task_repo.get_one({"entity_id": entity_id})
        return task

    def create_task(self, title: str, description: str):
        task = Task(
            title=title,
            description=description,
        )
        task = self.task_repo.add_task(task)
        return task

    def get_tasks_by_person_id(self, entity_id: str):
        tasks = self.task_repo.get_tasks_by_person_id(entity_id)
        return tasks
    
    def update_task(self, task: Task):
        task = self.task_repo.update_task(task)
        return task

    def mark_as_complete(self, task: Task):
        task.is_complete = True
        task = self.task_repo.update_task(task)
        return task