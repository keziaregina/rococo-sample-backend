import pika
import json
import time
from pika.exchange_type import ExchangeType
from mailjet_rest import Client

from common.app_config import config
from common.app_logger import logger

def get_mailjet_client() -> Client:
    return Client(
        auth=(config.MAILJET_API_KEY, config.MAILJET_API_SECRET), 
        version='v3.1'
    )

def send_email_via_mailjet(to_emails: list, event_name: str, event_data: dict):
    mailjet = get_mailjet_client()
    
    event_config = get_event_config(event_name)
    if not event_config:
        logger.error(f"Event configuration not found: {event_name}")
        raise ValueError(f"Event {event_name} not configured")
    
    variables = map_event_variables(event_name, event_data, event_config)

    logger.info("variables")
    logger.info(variables)
    
    recipients = []
    for email in to_emails:
        recipient = {
            "Email": email,
            "Variables": variables
        }
        recipients.append(recipient)
    
    message = {
        "From": {
            "Email": event_config.get("from_email", config.MAILJET_MAIL_FROM),
            "Name": event_config.get("from_name", config.MAILJET_MAIL_FROM_NAME)
        },
        "To": recipients,
        "TemplateID": event_config["template_id"],
        "TemplateLanguage": True,
        "subject": event_config["subject"],
        "Variables": variables
    }
    
    data = {'Messages': [message]}

    try:
        result = mailjet.send.create(data=data)
        logger.info(f"Email sent successfully to {to_emails} for event {event_name}")
        return result
    except Exception as e:
        logger.error(f"Failed to send email for event {event_name}: {str(e)}")
        raise


def get_event_config(event_name: str) -> dict:
    events_config = {
        "WELCOME_EMAIL": {
            "subject": "Welcome {{var:recipient_name}}",
            "template_id": config.MAILJET_WELCOME_EMAIL_TEMPLATE_ID,
            "from_email": config.MAILJET_MAIL_FROM,
            "from_name": config.MAILJET_MAIL_FROM_NAME,
            "variables_mapping": {
                "recipient_name": "recipient_name",
                "confirmation_link": "confirmation_link"
            }
        },
        "RESET_PASSWORD": {
            "subject": "Reset your password",
            "template_id": config.MAILJET_RESET_PASSWORD_TEMPLATE_ID,
            "from_email": config.MAILJET_MAIL_FROM,
            "from_name": config.MAILJET_MAIL_FROM_NAME,
            "variables_mapping": {
                "reset_password_link": "reset_password_link"
            }
        }
    }
    
    return events_config.get(event_name)


def map_event_variables(event_name: str, event_data: dict, event_config: dict) -> dict:
    variables = {}
    variables_mapping = event_config.get("variables_mapping", {})
    
    for template_var, data_key in variables_mapping.items():
        variables[template_var] = event_data.get(data_key, "")
    
    return variables


def process_email_message(message_data: dict):
    event = message_data.get("event")
    data = message_data.get("data", {})
    to_emails = message_data.get("to_emails", [])
    
    if not event:
        logger.error("Event name not provided in message")
        return
    
    if not to_emails:
        logger.error(f"No recipients provided for event {event}")
        return
    
    try:
        send_email_via_mailjet(
            to_emails=to_emails,
            event_name=event,
            event_data=data
        )
        logger.info("event name")
        logger.info(event)
        logger.info("event data")
        logger.info(data)
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        raise

def get_connection_parameters() -> pika.ConnectionParameters:
    return pika.ConnectionParameters(
        host=config.RABBITMQ_HOST,
        port=config.RABBITMQ_PORT,
        virtual_host=config.RABBITMQ_VIRTUAL_HOST,
        credentials=pika.credentials.PlainCredentials(
            username=config.RABBITMQ_USER,
            password=config.RABBITMQ_PASSWORD
        )
    )

def establish_connection(parameters: pika.ConnectionParameters, max_retries: int = 10) -> pika.BlockingConnection:
    retries = 0
    while retries < max_retries:
        try:
            connection = pika.BlockingConnection(parameters)
            return connection
        except Exception as e:
            logger.debug(f"Could not connect to messaging system. Retries {retries}")
            retries += 1
            if retries < max_retries:
                time.sleep(2 ** retries)
            else:
                logger.error("Error connecting to RabbitMQ after multiple retries")
                raise e

class MessageSender:
    def __init__(self):
        self.parameters = get_connection_parameters()

    def send_message(self, queue_name: str, data: dict, properties: pika.BasicProperties = None, exchange_name: str = None) -> None:
        """
        Sends a message to the specified RabbitMQ queue.

        :param queue_name: Name of the RabbitMQ queue to send the message to.
        :param data: The data to send to the queue as a dictionary.
        :return: None
        """
        connection = establish_connection(self.parameters)

        with connection:
            channel = connection.channel()

            if properties is None:
                properties = pika.BasicProperties(
                    delivery_mode=2,  # Make the message persistent
                )

            if exchange_name is None:
                exchange_name = ""
            else:
                channel.exchange_declare(exchange=exchange_name, exchange_type=ExchangeType.topic.value, durable=True)

            channel.queue_declare(queue=queue_name, durable=True)
            channel.basic_publish(
                exchange=exchange_name,
                routing_key=queue_name,
                body=json.dumps(data).encode(),
                properties=properties,
            )
            logger.info(f"Sent message to queue: {queue_name}")

class EmailConsumer:
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.parameters = get_connection_parameters()
    
    def callback(self, ch, method, properties, body):
        try:
            message_data = json.loads(body.decode())
            logger.info(f"Processing email message: {message_data.get('event')}")
            
            process_email_message(message_data)
            
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f"Email processed successfully")
            
        except Exception as e:
            logger.error(f"Error processing email message: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    def start_consuming(self):
        connection = establish_connection(self.parameters)
        channel = connection.channel()
        
        channel.queue_declare(queue=self.queue_name, durable=True)
        
        channel.basic_qos(prefetch_count=1)
        
        channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.callback
        )
        
        logger.info(f"Started consuming from queue: {self.queue_name}")
        
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("Stopping consumer")
            channel.stop_consuming()
        finally:
            connection.close()

if __name__ == "__main__":
    queue_name = config.QUEUE_NAME_PREFIX + config.EMAIL_SERVICE_PROCESSOR_QUEUE_NAME
    consumer = EmailConsumer(queue_name)
    consumer.start_consuming()
