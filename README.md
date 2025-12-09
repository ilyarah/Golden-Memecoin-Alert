# Golden Memecoin Alert

**A high-performance, real-time memecoin monitoring and alerting system for the TON blockchain.**

Golden Memecoin Alert continuously monitors selected Telegram channels for new Jetton (memecoin) launches, extracts contract addresses, performs on-chain verification, calculates a quality score, and delivers formatted alerts with direct trading links.

The project is structured as both a standalone sniper bot and a reusable Python package, enabling easy integration into larger monitoring or trading systems.

## Key Features

- Real-time message monitoring via Telethon  
- Automatic detection of TON Jetton contract addresses  
- On-chain verification (liquidity pool size, LP lock status, ownership renouncement, holder distribution)  
- Scoring engine combining technical and sentiment factors  
- Rich Telegram alerts with Markdown formatting and inline “Buy” button (DeDust)  
- Fully modular design with clean public API  
- Configuration via environment variables (`.env`)  

## Installation

```bash
git clone https://github.com/ilyarah/Golden-Memecoin-Alert.git
cd Golden-Memecoin-Alert
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your credentials and target channels, then launch:

```bash
python -m golden_memecoin_alert.main
```

## Configuration (`.env`)

```env
TELEGRAM_API_ID=2040
TELEGRAM_API_HASH=b18441a1ff607e10a989891a5462e627
TELEGRAM_BOT_TOKEN=your_bot_token
USER_CHAT_ID=your_telegram_id
CHANNELS=@ton_announcements,@meme_moguls,@airdropfam
MIN_LP_SIZE=70
SCORE_THRESHOLD=65
```

## Project Structure

```
golden_memecoin_alert/
├── main.py        → Entry point
├── config.py      → Configuration loading (Pydantic)
├── detector.py    → Message parsing and candidate extraction
├── verifier.py    → On-chain and API-based validation
├── scorer.py      → Scoring logic and sentiment analysis
├── notifier.py    → Alert formatting and delivery
└── __init__.py    → Package exports
```

## Usage as a Library

```python
from golden_memecoin_alert import Config, Detector, Verifier, Scorer, Notifier

config = Config()
# Components can be used independently in custom workflows
```

## Dependencies

Listed in `requirements.txt`:

- telethon
- python-telegram-bot
- aiohttp
- pydantic
- python-dotenv
- textblob

## License

Released under the MIT License. See `LICENSE` for details.

---
© 2025 ilyarah. All rights reserved.
