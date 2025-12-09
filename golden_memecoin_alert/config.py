import os
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import datetime

load_dotenv()  # reads the .env file

class Config(BaseModel):
    telegram_api_id: int = int(os.getenv("TELEGRAM_API_ID", "0"))
    telegram_api_hash: str = os.getenv("TELEGRAM_API_HASH", "")
    telegram_session: str = "my_session"  # will create a file called my_session.session
    channels: list = [c.strip() for c in os.getenv("CHANNELS", "").split(",") if c.strip()]
    score_threshold: float = float(os.getenv("SCORE_THRESHOLD", "70"))
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    user_chat_id: int = int(os.getenv("USER_CHAT_ID", "0"))
    min_lp_size: float = float(os.getenv("MIN_LP_SIZE", "100"))
    max_top_holder_pct: float = float(os.getenv("MAX_TOP_HOLDER_PCT", "10"))

class Candidate(BaseModel):  # shorter name, i'm lazy
    address: str
    message_text: str
    channel: str
    timestamp: datetime
    data: dict = {}
    score: float = 0.0
    breakdown: dict = {}
    sentiment: float = 0.0
    ok: bool = True