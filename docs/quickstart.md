# Quickstart

By default the `http_handler` decorator makes sure of parsing the request body
as JSON, and also formats the response as JSON with:
    - an adequate statusCode,
    - CORS headers, and
    - the handler return value in the body.

```python
from lambda_handlers.handlers import http_handler

@http_handler()
def handler(event, context):
    return event['body']
```
