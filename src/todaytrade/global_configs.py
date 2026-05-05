import logging
from pathlib import Path
from todaytrade.utils.load_utils import load_yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIGS_PATH = PROJECT_ROOT / "configs"

CLIENTS_CONFIG = load_yaml(CONFIGS_PATH / "clients.yaml")
MOOMOO_CLIENT_CONFIG = CLIENTS_CONFIG["MOOMOO_CLIENT"]