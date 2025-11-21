from common.services.task import TaskService
from flask import request
from flask_restx import Namespace, Resource
from app.helpers.response import get_success_response, parse_request_body, validate_required_fields
from app.helpers.decorators import login_required
from common.app_config import config
from common.models.task import Task

# Create the organization blueprint
task_api = Namespace('task', description="Task-related APIs")

@task_api.route('/create')
class Create(Resource):
    @task_api.expect(
        {'type': 'object', 'properties': {
            'title': {'type': 'string'},
            'description': {'type': 'string'},
        }}
    )
    def post(self):
        parsed_body = parse_request_body(request, ['title', 'description'])
        validate_required_fields(parsed_body)
        task_service = TaskService(config)
        task = task_service.create_task(parsed_body['title'], parsed_body['description'])
        return get_success_response(message="Task created successfully.", task=task)

@task_api.route('/list/<person_id>')
class List(Resource):
    def get(self, person_id):
        is_complete = request.args.get('is_complete', None)
        task_service = TaskService(config)
        tasks = task_service.get_tasks_by_person_id(person_id, is_complete)
        return get_success_response(tasks=tasks)

@task_api.route('/update/<task_id>')
class Update(Resource):
    @task_api.expect(
        {'type': 'object', 'properties': {
            'title': {'type': 'string'},
            'description': {'type': 'string'},
        }}
    )
    def put(self, task_id):
        parsed_body = parse_request_body(request, ['title', 'description'])
        validate_required_fields(parsed_body)
        task_service = TaskService(config)
        task = task_service.get_task_by_id(task_id)
        task.title = parsed_body['title']
        task.description = parsed_body['description']
        task = task_service.update_task(task)
        return get_success_response(message="Task updated successfully.", task=task)

@task_api.route('/delete/<task_id>')
class Delete(Resource):
    def delete(self, task_id):
        task_service = TaskService(config)
        task = task_service.get_task_by_id(task_id)
        print ("task", task)
        task_service.delete_task(task)
        return get_success_response(message="Task deleted successfully.", task=task)

@task_api.route('/complete/<task_id>')
class Complete(Resource):
    def put(self, task_id):
        task_service = TaskService(config)
        task = task_service.get_task_by_id(task_id)
        task.is_complete = True
        task = task_service.mark_as_complete(task)
        return get_success_response(message="Task completed successfully.", task=task)

@task_api.route('/incomplete/<task_id>')
class Incomplete(Resource):
    def put(self, task_id):
        task_service = TaskService(config)
        task = task_service.get_task_by_id(task_id)
        task.is_complete = False
        task = task_service.mark_as_incomplete(task)
        return get_success_response(message="Task incomplete successfully.", task=task)

@task_api.route('/find/<task_id>')
class Task(Resource):
    def get(self, task_id):
        task_service = TaskService(config)
        task = task_service.get_task_by_id(task_id)
        print ("task", task)
        return get_success_response(task=task)