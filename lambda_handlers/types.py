"""Declaration of types through the project."""

from typing import Any, Dict, Union, Optional
from dataclasses import asdict, dataclass

Headers = Dict[str, Union[str, bool, int]]


@dataclass
class APIGatewayProxyResult:
    """Key names are expected and given by AWS APIGateway specifications and must not be changed."""

    statusCode: int
    body: Union[str, Dict[str, Any]]
    headers: Optional[Headers] = None
    multiValueHeaders: Optional[Headers] = None
    isBase64Encoded: Optional[bool] = None

    def asdict(self) -> Dict[str, Any]:
        """Convert self into a dict."""
        return {k: v for k, v in asdict(self).items() if v is not None}
