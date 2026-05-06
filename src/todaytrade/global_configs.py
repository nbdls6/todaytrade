import logging
from pathlib import Path
from todaytrade.utils.load_utils import load_yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIGS_PATH = PROJECT_ROOT / "configs"
DATA_PATH = PROJECT_ROOT / "data"

DATA_CONFIGS = load_yaml(CONFIGS_PATH / "data_configs.yaml")
EVENT_DATA_CONFIG = DATA_CONFIGS["EVENT_DATA"]
EVENT_DATA_DIR = DATA_PATH / EVENT_DATA_CONFIG["DATA_DIR"]
EVENT_DATA_LOG_FILE = EVENT_DATA_CONFIG["EVENT_LOG_FILE"]
EVENT_DATA_LOG_FILE_PATH = EVENT_DATA_DIR / EVENT_DATA_LOG_FILE
KLINE_DATA_DIR = EVENT_DATA_DIR / EVENT_DATA_CONFIG["KLINE_DATA"]["DATA_DIR"]
KLINE_1M_DATA_DIR = KLINE_DATA_DIR / EVENT_DATA_CONFIG["KLINE_DATA"]["1M_DATA_DIR"]

CLIENT_CONFIGS = load_yaml(CONFIGS_PATH / "client_configs.yaml")
MOOMOO_CLIENT_CONFIG = CLIENT_CONFIGS["MOOMOO_CLIENT"]