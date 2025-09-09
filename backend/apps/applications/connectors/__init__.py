from .base import ConnectorBase
from .greenhouse import GreenhouseConnector
from .lever import LeverConnector

CONNECTORS = {
    "greenhouse": GreenhouseConnector,
    "lever": LeverConnector,
}

def get_connector(key: str):
    return CONNECTORS.get(key)

