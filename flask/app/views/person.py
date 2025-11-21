from common.models.person import Person
from common.services.person import PersonService
from flask import request
from flask_restx import Namespace, Resource
from app.helpers.response import get_success_response, parse_request_body, validate_required_fields
from app.helpers.decorators import login_required
from common.app_config import config

# Create the organization blueprint
person_api = Namespace('person', description="Person-related APIs")


@person_api.route('/me/<person_id>')
class Me(Resource):
    
    # @login_required()
    def get(self, person_id):
        person_service = PersonService(config)
        person = person_service.get_person_by_id(person_id)
        return get_success_response(person=person)

@person_api.route('/me/update/<person_id>')
class update(Resource):
    @person_api.expect(
        {'type': 'object', 'properties': {
            # 'person_id': {'type': 'string'},
            'first_name': {'type': 'string'},
            'last_name': {'type': 'string'},
        }}
    )
    def put(self, person_id):
        parsed_body = parse_request_body(request, ['first_name', 'last_name'])
        validate_required_fields(parsed_body)

        person_service = PersonService(config)
        person = person_service.get_person_by_id(person_id)
        print('test')
        # person.entity_id = person_id
        person.first_name = parsed_body['first_name']
        person.last_name = parsed_body['last_name']
        person_service.update_person(person)
        return get_success_response(message="Person updated successfully.", person=person)

@person_api.route('/all')
class All(Resource):
    def get(self):
        person_service = PersonService(config)
        persons = person_service.get_all_persons()
        return get_success_response(persons=persons)

@person_api.route('/delete/<person_id>')
class Delete(Resource):
    def delete(self, person_id):
        person_service = PersonService(config)
        person = person_service.get_person_by_id(person_id)
        person_service.delete_person(person)
        return get_success_response(message="Person deleted successfully.", person=person)

@person_api.route('/create')
class Create(Resource):
    def post(self):
        parsed_body = parse_request_body(request, ['first_name', 'last_name'])
        validate_required_fields(parsed_body)

        person_service = PersonService(config)
        person = person_service.create_person(parsed_body['first_name'], parsed_body['last_name'])
        return get_success_response(message="Person created successfully.", person=person)