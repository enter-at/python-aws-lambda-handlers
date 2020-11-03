### Headers

#### Cors

```python
from lambda_handlers.handlers import http_handler
from lambda_handlers.response import cors

@http_handler(cors=cors(origin='example.com', credentials=False))
def handler(event, context):
    return {
        'message': 'Hello World!'
    }
```

```bash
aws lambda invoke --function-name example response.json
cat response.json
```

```json
{
    "headers":{
        "Access-Control-Allow-Origin": "example.com",
        "Content-Type": "application/json"
    },
    "statusCode": 200,
    "body": "{\"message\": \"Hello World!\"}"
}
```
