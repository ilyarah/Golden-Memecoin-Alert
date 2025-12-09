import asyncio
import logging
from telethon import TelegramClient, events
from telegram import Bot
from golden_memecoin_alert.config import Config
from golden_memecoin_alert.detector import Detector
from golden_memecoin_alert.verifier import Verifier
from golden_memecoin_alert.scorer import Scorer
from golden_memecoin_alert.notifier import Notifier

logging.basicConfig(level=logging.INFO)

async def main():
    cfg = Config()
    
    # This time we use real API ID + HASH + phone login (one-time only)
    client = TelegramClient('golden_session', cfg.telegram_api_id, cfg.telegram_api_hash)
    
    # Bot for sending alerts
    alert_bot = Bot(token=cfg.telegram_bot_token)

    q = asyncio.Queue(maxsize=50)
    seen = set()
    cache = {}

    detector = Detector(client, cfg.channels, q, seen, cfg)
    verifier = Verifier(cfg, cache)
    scorer = Scorer(cfg)
    notifier = Notifier(alert_bot, cfg)

    async def worker():
        while True:
            cand = await q.get()
            cand = await verifier.verify(cand)
            if cand.ok:
                cand = scorer.score(cand)
                await notifier.send(cand)
            q.task_done()

    await client.start()                     # ← will ask phone + code ONLY the first time
    print("Bot is alive and watching your channels!")
    
    await asyncio.gather(
        detector.start(),
        worker()
    )

if __name__ == "__main__":
    asyncio.run(main())