from lambda_handlers.validators.http.http_validator import HttpValidator
from lambda_handlers.validators.jsonschema_validator import JSONSchemaValidator


class HttpJSONSchemaValidator(JSONSchemaValidator, HttpValidator):
    pass
