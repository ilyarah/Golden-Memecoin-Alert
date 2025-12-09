import aiohttp
import asyncio
import logging
from .config import Candidate, Config

log = logging.getLogger("verifier")
BURN = "EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c"

class Verifier:
    def __init__(self, cfg, cache):
        self.cfg = cfg
        self.cache = cache

    async def verify(self, cand: Candidate) -> Candidate:
        addr = cand.address
        if addr in self.cache:
            cand.data = self.cache[addr]
            return cand

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            try:
                # try tonapi first (easiest)
                url = f"https://tonapi.io/v2/jettons/{addr}"
                async with session.get(url) as r:
                    if r.status == 200:
                        j = await r.json()
                        cand.data["name"] = j.get("metadata", {}).get("name", "Unknown")
                        cand.data["supply"] = int(j.get("total_supply", 0))
                        admin = j.get("admin_address", BURN)
                        cand.data["renounced"] = (admin == BURN)

                        # LP check on ston.fi
                        lp = await self.check_lp_ston(session, addr)
                        cand.data.update(lp)

                        # top holder %
                        holders = await self.top_holder(session, addr)
                        cand.data["top_holder_pct"] = holders

                        self.cache[addr] = cand.data.copy()
                        log.info(f"Verified {addr} – LP {lp.get('lp_size',0):.1f} TON")
                        return cand
            except Exception as e:
                log.warning(f"Verification failed for {addr}: {e}")

        cand.ok = False
        return cand

    async def check_lp_ston(self, session, jetton):
        try:
            payload = {"token0": "TON", "token1": jetton}
            async with session.post("https://api.ston.fi/v1/pools", json=payload) as r:
                if r.status == 200:
                    data = await r.json()
                    if data.get("pools"):
                        pool = data["pools"][0]
                        ton_reserve = float(pool["reserve0"]) / 1e9
                        locked = pool.get("lp_burned", False)
                        return {"lp_size": ton_reserve, "locked": locked}
        except:
            pass
        return {"lp_size": 0, "locked": False}

    async def top_holder(self, session, addr):
        try:
            async with session.get(f"https://tonapi.io/v2/jettons/{addr}/holders?limit=1") as r:
                if r.status == 200:
                    j = await r.json()
                    top = j["holders"][0]["balance"]
                    supply = j["total_supply"]
                    return (int(top) / int(supply)) * 100
        except:
            return 100
        return 100