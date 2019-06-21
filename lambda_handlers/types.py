from dataclasses import dataclass, asdict
from typing import Dict, Union, Optional


@dataclass
class APIGatewayProxyResult:
    """
    Key names are expected and given by AWS APIGateway specifications and must not be changed
    """
    statusCode: int
    body: str
    headers: Optional[Dict[str, Union[bool, str, int]]] = None
    multiValueHeaders: Optional[Dict[str, Union[bool, str, int]]] = None
    isBase64Encoded: bool = None

    def asdict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
