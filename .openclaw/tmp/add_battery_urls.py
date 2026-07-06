#!/usr/bin/env python3
"""Add purchaseUrl to all battery candidates in candidates.sysml"""
import re

PATH = "/home/david12daniel/.openclaw/agents/thermal-surveillance-drone/candidates.sysml"

battery_urls = {
    "BAT01": "https://www.racedayquads.com/products/lumenier-nav-10000mah-6s-21700-lithium-ion-battery-xt60",
    "BAT02": "https://www.upgrade-energy.com/",
    "BAT03": "https://www.upgrade-energy.com/",
    "BAT04": "https://www.racedayquads.com/products/lumenier-nav-12000mah-4s-21700-amprius-lithium-ion-battery-xt60",
    "BAT05": "https://pyrodrone.com/products/gaoneng-gnb-8000mah-22-2v-6s-10c-6s2p-made-with-samsung-21700-40t-long-range-cinelifter-lipo-battery-xt60",
    "BAT06": "https://pyrodrone.com/products/iflight-fullsend-e-6s-8000mah-22-2v-6s1p-lipo-battery-xt60",
    "BAT07": "https://www.upgrade-energy.com/",
    "BAT08": "https://www.racedayquads.com/products/lumenier-nav-12000mah-6s-21700-lithium-ion-battery-xt90",
    "BAT09": "https://www.racedayquads.com/products/lumenier-nav-12000mah-6s-21700-amprius-lithium-ion-battery-xt60",
    "BAT10": "https://www.upgrade-energy.com/",
    "BAT11": "https://www.upgrade-energy.com/",
    "BAT12": "https://www.upgrade-energy.com/",
    "BAT13": "https://pyrodrone.com/products/pyrodrone-hyperjuice-6000mah-6s2p-li-ion-long-range-battery-xt60",
    "BAT14": "https://shop.iflight.com/",
    "BAT15": "https://www.racedayquads.com/products/lumenier-nav-22-2v-6s-18650-6000mah-10c-li-ion-battery-xt60",
    "BAT16": "https://www.upgrade-energy.com/",
    "BAT17": "https://www.upgrade-energy.com/",
    "BAT18": "https://www.racedayquads.com/products/lumenier-nav-8000mah-4s-18650-amprius-lithium-ion-battery-xt60",
    "BAT19": "https://www.racedayquads.com/products/lumenier-nav-5000mah-6s-21700-lithium-ion-battery-xt60",
    "BAT20": "https://www.upgrade-energy.com/",
    "BAT21": "https://www.aliexpress.com/wholesale?SearchText=DOGCOM+5000mAh+Samsung+50S",
}

with open(PATH, 'r') as f:
    content = f.read()

changes = 0
for cid, url in battery_urls.items():
    pattern = re.compile(
        r'(  part ' + re.escape(cid) + r' : Battery \{\n   :>> name = "[^"]+";)'
    )
    match = pattern.search(content)
    if match:
        replacement = match.group(1) + f'\n   :>> purchaseUrl = "{url}";'
        content = content[:match.start(1)] + replacement + content[match.end(1):]
        changes += 1
        print(f"  ADD URL {cid}: {url}")
    else:
        print(f"  WARNING: Could not find {cid}")

with open(PATH, 'w') as f:
    f.write(content)

print(f"\nAdded {changes} battery URLs")
