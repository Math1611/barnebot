import os
from dotenv import load_dotenv

load_dotenv()

WA_TOKEN = os.getenv("WA_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

LAT = float(os.getenv("LAT"))
LON = float(os.getenv("LON"))
