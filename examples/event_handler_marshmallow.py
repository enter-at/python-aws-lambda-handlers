from lambda_handlers import validators
from lambda_handlers.handlers import event_handler
from marshmallow import Schema, fields, validates_schema
from marshmallow.validate import Range, ValidationError


class EventSchema(Schema):
    price = fields.Integer(required=True, validate=Range(min=1, max=100))
    timestamp = fields.Date(required=True)


class NotOptionalEventSchema(EventSchema):
    @validates_schema
    def payload_validator(self, data):
        if data is None:
            raise ValidationError('Invalid payload')


class ResponseSchema(Schema):
    message = fields.String(required=True)


@event_handler(
    validator=validators.marshmallow(
        input_schema=NotOptionalEventSchema(),
        output_schema=ResponseSchema(),
    ),
)
def handler(event, context):
    price = event['price']
    timestamp = event['timestamp']
    return {
        'message': f'The price on {timestamp} is {price}.'
    }
