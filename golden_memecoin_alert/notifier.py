
# ======================================================
#  GOLDEN MEMECOIN ALERT — NOTIFIER (the sexiest one alive)
#  Bot name: @GoldenMemecoinAlertBot  (or whatever you chose)
# ======================================================

from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
import logging

log = logging.getLogger("golden_notifier")

class Notifier:
    def __init__(self, bot: Bot, cfg):
        self.bot = bot
        self.cfg = cfg

    async def send(self, cand):
        if cand.score < self.cfg.score_threshold:
            return

        # ——— SCORE FIREWORKS ———
        fire_level = cand.score // 15
        fire = "🔥" * fire_level
        rocket = "🚀🚀🚀" if cand.score >= 95 else "🚀🚀" if cand.score >= 85 else "🚀"

        hype_words = {
            0.8: "RETARDS ARE APING LIKE MAD",
            0.6: "FOMO IS BUILDING HARD",
            0.4: "whales sniffing",
            0.0: "still early, chill"
        }
        hype_text = next((v for k, v in hype_words.items() if cand.sentiment >= k), "warming up")

        message = f"""*{rocket} GOLDEN MEMECOIN ALERT {rocket}*

*GEM DETECTED & VERIFIED*

🪙 *Name:* `{cand.data.get('name', 'Hidden Alpha')}`
📍 *Contract Address:*
`{cand.address}`

💧 *Liquidity:* `{cand.data.get('lp_size',0):.1f} TON` {'🔒 LOCKED FOREVER' if cand.data.get('locked') else '⚠️ unlocked'}
👑 *Ownership:* {'RENounced — based dev ✅' if cand.data.get('renounced') else '⚠️ still owned'}

⚡ *GOLDEN SCORE:* `{cand.score}/100` {fire}
😤 *Hype Level:* `{hype_text.upper()}`

⏰ Watch 3–5 min → if no dump → ape responsibly
💎 *Instant Buy → DeDust*
https://dedust.io/swap/TON/{cand.address}

Powered by **Golden Memecoin Alert** — your personal 100x sniper

_Another gem cooked. Stay golden._ ✨"""

        # ——— ONE-CLICK BUY BUTTON ———
        buy_button = InlineKeyboardMarkup([[
            InlineKeyboardButton("BUY NOW — SEND IT 🚀", url=f"https://dedust.io/swap/TON/{cand.address}")
        ]])

        try:
            await self.bot.send_message(
                chat_id=self.cfg.user_chat_id,
                text=message,
                parse_mode="Markdown",
                reply_markup=buy_button,
                disable_web_page_preview=True
            )
            log.info(f"GOLDEN ALERT FIRED → {cand.address} | Score: {cand.score}")
        except Exception as e:
            log.error(f"Failed to deliver golden alert: {e}")