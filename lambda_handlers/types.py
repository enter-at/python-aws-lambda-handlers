from typing import Any, Dict, Union, Optional
from dataclasses import asdict, dataclass

Headers = Optional[Dict[str, Union[str, bool, int]]]


@dataclass
class APIGatewayProxyResult:
    """
    Key names are expected and given by AWS APIGateway specifications and must not be changed
    """
    statusCode: int
    body: Union[str, Dict[str, Any]]
    headers: Headers = None
    multiValueHeaders: Headers = None
    isBase64Encoded: Optional[bool] = None

    def asdict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
