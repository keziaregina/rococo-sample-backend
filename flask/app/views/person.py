from common.models.person import Person
from common.services.person import PersonService
from flask import request
from flask_restx import Namespace, Resource
from app.helpers.response import get_success_response, parse_request_body, validate_required_fields
from app.helpers.decorators import login_required
from common.app_config import config

# Create the organization blueprint
person_api = Namespace('person', description="Person-related APIs")


@person_api.route('/me')
class Me(Resource):
    
    @login_required()
    def get(self, person):
        return get_success_response(person=person)

@person_api.route('/me/update')
class update(Resource):
    @login_required()
    @person_api.expect(
        {'type': 'object', 'properties': {
            'first_name': {'type': 'string'},
            'last_name': {'type': 'string'}, 
        }}
    )
    def put(self, person):
        parsed_body = parse_request_body(request, ['first_name', 'last_name'])
        validate_required_fields(parsed_body)

        person_service = PersonService(config)
        person.first_name = parsed_body['first_name']
        person.last_name = parsed_body['last_name']
        person_service.update_person(person)
        return get_success_response(message="Person updated successfully.", person=person)

@person_api.route('/all')
class All(Resource):
    @login_required()
    def get(self, person):
        person_service = PersonService(config)
        persons = person_service.get_all_persons()
        return get_success_response(persons=persons)

@person_api.route('/create')
class Create(Resource):
    def post(self):
        parsed_body = parse_request_body(request, ['first_name', 'last_name'])
        validate_required_fields(parsed_body)

        person_service = PersonService(config)
        person = Person(
            first_name=parsed_body['first_name'],
            last_name=parsed_body['last_name'],
        )
        person = person_service.save_person(person)
        return get_success_response(message="Person created successfully.", person=person)