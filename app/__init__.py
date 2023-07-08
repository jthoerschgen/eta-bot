import argparse
from decouple import config
import logging
import os

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("--testing", help="Uses Testing Settings", action="store_true")
args = parser.parse_args()

# Set enviornment variables
os.environ["GROUP_ME_TOKEN"] = config("GROUP_ME_TOKEN")
if args.testing:
    os.environ["BOT_NAME"]: str = config("BOT_NAME_TESTING")
    os.environ["GROUP_ID"]: int = config("GROUP_ID_TESTING")
    os.environ["BOT_ID"]: str = config("BOT_ID_TESTING")
elif not args.testing:
    os.environ["BOT_NAME"]: str = config("BOT_NAME")
    os.environ["GROUP_ID"]: int = config("GROUP_ID")
    os.environ["BOT_ID"]: str = config("BOT_ID")
