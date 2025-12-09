import re
import asyncio
import logging
from datetime import datetime
from telethon import TelegramClient, events
from .config import Candidate, Config

log = logging.getLogger("detector")

class Detector:
    def __init__(self, client, channels, queue, seen, cfg):
        self.client = client
        self.channels = channels
        self.queue = queue
        self.seen = seen
        self.cfg = cfg

    async def start(self):
        @self.client.on(events.NewMessage(chats=self.channels))
        async def handler(event):
            msg = event.message.message or ""
            # ignore old messages when bot restarts
            if (datetime.now() - event.message.date).total_seconds() > 3600:
                return

            # look for EQ... address
            match = re.search(r'EQ[a-zA-Z0-9_-]{46}', msg)
            if not match:
                return
            addr = match.group(0)

            # basic keywords so we don't react to random crap
            keywords = ["launch", "new", "memecoin", "pump", "just launched"]
            if not any(k in msg.lower() for k in keywords):
                return

            if addr in self.seen:
                return
            self.seen.add(addr)

            cand = Candidate(
                address=addr,
                message_text=msg,
                channel=event.chat.title or "unknown",
                timestamp=event.message.date
            )
            await self.queue.put(cand)
            log.info(f"→ Found new coin: {addr}")

        log.info("Detector is listening...")
        await self.client.start()
        await self.client.run_until_disconnected()