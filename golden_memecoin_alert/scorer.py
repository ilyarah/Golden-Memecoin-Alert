from textblob import TextBlob
from .config import Candidate, Config

class Scorer:
    def __init__(self, cfg: Config):
        self.cfg = cfg

    def score(self, cand: Candidate) -> Candidate:
        if not cand.ok:
            return cand

        total = 0
        breakdown = {}

        # LP size
        if cand.data.get("lp_size", 0) >= self.cfg.min_lp_size:
            total += 25
            breakdown["lp"] = 25

        # LP locked/burned
        if cand.data.get("locked"):
            total += 20
            breakdown["lock"] = 20

        # owner renounced
        if cand.data.get("renounced"):
            total += 15
            breakdown["renounced"] = 15

        # no obvious honeypot (we keep it simple)
        breakdown["no_honeypot"] = 15
        total += 15

        # top holder not too big
        if cand.data.get("top_holder_pct", 100) <= self.cfg.max_top_holder_pct:
            total += 15
            breakdown["diversity"] = 15

        # sentiment from the telegram message
        try:
            sent = TextBlob(cand.message_text).sentiment.polarity
            cand.sentiment = sent
            if sent > 0.5:
                total += 20
                breakdown["hype"] = 20
        except:
            pass

        cand.score = min(total, 100)
        cand.breakdown = breakdown
        return cand