import logging
from pathlib import Path
from todaytrade.utils.load_utils import load_yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIGS_PATH = PROJECT_ROOT / "configs"

MOOMOO_CLIENT = clients_config["MOOMOO_CLIENT"]