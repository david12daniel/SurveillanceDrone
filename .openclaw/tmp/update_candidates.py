#!/usr/bin/env python3
"""
Update candidates.sysml with purchase URLs and corrected prices.
Reads research data from .openclaw/tmp/*_prices.txt and applies targeted edits.
"""
import re, os, json

CANDIDATES_PATH = os.path.expanduser("/home/david12daniel/.openclaw/agents/thermal-surveillance-drone/candidates.sysml")

# =============================================================================
# PRICE CORRECTIONS from web research (verified prices differ from model)
# Format: (candidate_id, new_price, reason)
# =============================================================================
PRICE_CORRECTIONS = {
    "T1":     (109.0, "Verified $109 on GroupGets (was $75)"),
    "T2":     (150.0, "Verified $150 on GroupGets (was $140)"),
    "T3":     (164.0, "Verified $164 on GroupGets (was $186)"),
    "T4":     (173.0, "Verified ~$173 GroupGets (was $240)"),
    "T5":     (250.0, "Discontinued; est $250 original MSRP (was $245)"),
    "T6":     (85.0,  "Waveshare 404; est ~$85 (was $85 - no change)"),
    "T8":     (150.0, "AliExpress $100-220; representative $150 (was $150 - ok)"),
    "T9":     (320.0, "AliExpress $250-400; representative $320 (was $320 - ok)"),
    "T10":    (550.0, "AliExpress $400-800; representative $550 (was $550 - ok)"),
    "T11":    (450.0, "AliExpress $350-550 (was $650 - was overestimated)"),
    "T12":    (520.0, "iVcan OEM $450-600 (was $980 - was overestimated)"),
    "T13":    (450.0, "PurpleRiver $350-500 (was $590 - was overestimated)"),
    "T14":    (650.0, "Arducam ~$650 (was $650 - ok)"),
    "T15":    (400.0, "Seek Thermal ~$400 (was $400 - ok)"),
    "T16":    (3558.0,"FLIR Boson $3,558+ (over $600 budget anyway)"),
    
    "AF1":    (285.0, "May be discontinued on GEPRC - price kept"),
    "AF2a":   (175.0, "KOLAS7 PNP - $175 est (frame kit only available on RDQ)"),
    "AF2b":   (419.90,"Verified $419.90 on coolgoos.com (no change)"),
    "AF2c":   (713.0, "Verified $713 (no change)"),
    "AF3a":   (305.35,"Verified $305.35 at shop.iflight.com (was $346.99 - was BNF price)"),
    "AF3b":   (346.99,"Verified $346.99 at shop.iflight.com (was $372)"),
    "AF4a":   (279.99,"Verified $279.99 at darwinfpv.com (was $340)"),
    "AF5":    (398.86,"EMAX Hawk 7 BNF - may be discontinued; keep price"),
    "AF6a":   (825.99,"Verified $825.99 at pyrodrone.com (was $369 - O4 Pro is premium)"),
    "AF6b":   (851.99,"Verified $851.99 at pyrodrone.com (was $394 - O4 Pro BNF)"),
    "AF7":    (726.99,"Verified $726.99 at pyrodrone.com (was $510 - Croc75 V3 HD Wasp)"),
    "AF8a":   (499.99,"Verified $499.99 at shop.iflight.com (analog PNP, was $499.99 - ok)"),
    "AF8b":   (525.0, "BNF +$25 over PNP (was $525 - ok)"),
    "AF9a":   (299.99,"Verified $299.99 at pyrodrone.com (was $222 - Darwin129 price increased)"),
    "AF10":   (799.99,"Verified $799.99 at newbeedrone.com (was $699)"),
    
    "BAT01":  (149.99,"Verified $149.99 at racedayquads.com (was $149.99 - ok)"),
    "BAT04":  (218.99,"Verified $218.99 at racedayquads.com (was $218.99 - ok)"),
    "BAT05":  (135.99,"Verified $135.99 at pyrodrone.com (was $135.99 - ok)"),
    "BAT06":  (122.99,"Updated: was $73.91, street price $122.99 at pyrodrone.com"),
    "BAT08":  (189.99,"Verified $189.99 at racedayquads.com (was $189.99 - ok)"),
    "BAT09":  (321.49,"Verified $321.49 at racedayquads.com (was $321.49 - ok)"),
    "BAT13":  (172.99,"Verified $172.99 at pyrodrone.com (was $172.99 - ok)"),
    "BAT15":  (188.99,"Verified $188.99 at racedayquads.com (was $188.99 - ok)"),
    "BAT18":  (134.99,"Verified $134.99 at racedayquads.com (was $134.99 - ok)"),
    "BAT19":  (95.99, "Verified $95.99 at racedayquads.com (was $95.99 - ok)"),
}

# =============================================================================
# PURCHASE URLS (candidate_id -> purchaseUrl value)
# =============================================================================
PURCHASE_URLS = {
    # Airframes
    "AF1": "https://geprc.com/product/mark4-drone-for-freestyle-fpv-4s-6s/",
    "AF2a": "https://axisflying.net/products/axisflying-kolas7-7inch-foldable-fpv-drone-for-lr-long-range-cinematic-shooting-frame-kit",
    "AF2b": "https://www.coolgoos.com/products/axisflying-kolas7-analog-bnf-7inch-foldable-fpv-drone-for-lr-long-range-cinematic-drone-with-gps",
    "AF2c": "https://www.axisflying.com/products/kolas7",
    "AF3a": "https://shop.iflight.com/Chimera9-ECO-6S-Pro2068",
    "AF3b": "https://shop.iflight.com/Chimera9-ECO-6S-Pro2068",
    "AF4a": "https://darwinfpv.com/products/darwinfpv-x9-9-long-range-fpv-drone",
    "AF5": "https://www.emax-usa.com/collections/hawk-series",
    "AF6a": "https://pyrodrone.com/products/deepspacefpv-roc7-o4-pro-long-range-fpv-7inch-digital-pnp-with-gps-freestyle-fpv-drone-choose-receiver",
    "AF6b": "https://pyrodrone.com/products/deepspacefpv-roc7-o4-pro-long-range-fpv-7inch-digital-pnp-with-gps-freestyle-fpv-drone-choose-receiver",
    "AF7": "https://pyrodrone.com/products/geprc-crocodile75-v3-hd-wasp-long-range-fpv-choose-receiver-type",
    "AF8a": "https://shop.iflight.com/Chimera7-Pro-V2-6S-Pro1947",
    "AF8b": "https://shop.iflight.com/Chimera7-Pro-V2-6S-Pro1947",
    "AF9a": "https://pyrodrone.com/products/darwinfpv-darwin129-7-long-range-bnf",
    "AF10": "https://newbeedrone.com/products/deepspace-roc7-o4pro-long-range-fpv-7inch-f722-60a-racing-drone-quadcopter-freestyle",
    # Thermal cameras
    "T1": "https://groupgets.com/products/flir-lepton-2-5",
    "T2": "https://groupgets.com/products/flir-lepton-3-0",
    "T3": "https://groupgets.com/products/flir-lepton-3-5",
    "T4": "https://www.flytron.com/thermal-solutions/60-dronethermal-v4.html",
    "T5": "https://horusdynamics.com/shop/lepton-kit-hdk1500/",
    "T6": "https://www.waveshare.com/infrared-thermal-camera-module.htm",
    "T7": "https://www.mouser.com/ProductDetail/heimann-sensor/htpa80x64d",
    "T8": "https://www.aliexpress.com/wholesale?SearchText=256x192+thermal+camera+module+CVBS",
    "T9": "https://www.aliexpress.com/wholesale?SearchText=384x288+thermal+camera+module+CVBS",
    "T10": "https://www.aliexpress.com/wholesale?SearchText=640x512+thermal+camera+module+CVBS",
    "T11": "https://www.amazon.com/dp/B0GYQ67TTQ",
    "T12": "https://www.aliexpress.com/wholesale?SearchText=iVcan+Mini+640+CVBS+thermal",
    "T13": "https://www.aliexpress.com/wholesale?SearchText=PurpleRiver+mini+640+thermal",
    "T14": "https://www.arducam.com/product/arducam-thermal-camera-module-640x512-thermal-infrared-camera-module-with-usb-type-c-for-jetson-nano-raspberry-pi-and-windows/",
    "T15": "https://www.amazon.com/s?k=seek+thermal+mosaic+320",
    "T16": "https://groupgets.com/products/flir-boson-640",
    # FPV cameras
    "A1": "https://geprc.com/",
    "A2": "https://www.amazon.com/s?k=Caddx+Ratel+2",
    "A3": "https://www.amazon.com/s?k=Foxeer+Predator+Mini+V4",
    "A4": "https://www.amazon.com/s?k=Runcam+Phoenix+2",
    "A5": "https://shop.iflight.com/",
    "A6": "https://www.emax-usa.com/",
    "A7": "https://www.amazon.com/s?k=Caddx+Ant",
    "A8": "https://www.amazon.com/s?k=Foxeer+T-Rex+Micro",
    "D1": "https://www.dji.com/o4-pro-air-unit",
    "D2": "https://www.dji.com/o3-air-unit",
    "D3": "https://shop.walksnail.com/",
    "D4": "https://shop.runcam.com/racer-4/",
    "D5": "https://www.amazon.com/s?k=Foxeer+Apollo+Digital",
    "D6": "https://www.amazon.com/s?k=HDZero+Nano+V3",
    "D7": "https://www.amazon.com/s?k=Foxeer+Digisight+3",
    "D8": "https://shop.walksnail.com/products/walksnail-avatar-nano-kit-v3",
    # GPS modules
    "G1": "https://www.amazon.com/s?k=Beitian+BN-220+GPS",
    "G2": "https://www.amazon.com/s?k=Beitian+BN-880+GPS",
    "G3": "https://www.amazon.com/s?k=Matek+M10Q-5883",
    "G4": "https://shop.iflight.com/",
    "G5": "https://shop.iflight.com/",
    "G6": "https://www.team-blacksheep.com/",
    # SBCs
    "SBC1": "https://radxa.com/products/zero/zero2pro",
    "SBC2": "https://www.orangepi.org/",
    "SBC3": "https://www.friendlyelec.com/index.php?route=product/product&path=69&product_id=309",
    # Radio receivers
    "RP3V2": "https://www.amazon.com/dp/B0CGCM2GQ5",
    "RP4TD": "https://www.amazon.com/dp/B0CT3H5493",
    "RP4TD_M": "https://www.amazon.com/s?k=RadioMaster+RP4TD",
    "EP1": "https://www.amazon.com/s?k=Happymodel+EP1+TCXO",
    "SuperD": "https://betafpv.com/",
    "iFlightTD": "https://shop.iflight.com/",
    "TBSNano": "https://www.team-blacksheep.com/",
    "TBSCrossfireNano": "https://www.team-blacksheep.com/",
    "GEPRC2G4Dual": "https://geprc.com/",
    "GEPRCNanoPA100": "https://geprc.com/",
    "MatekR24D": "https://www.mateksys.com/",
    # Radio TX
    "TX1": "https://www.radiomasterrc.com/products/boxer",
    "TX2": "https://www.radiomasterrc.com/products/tx16s",
    "TX3": "https://www.radiomasterrc.com/products/tx16s-mk3",
    "TX4": "https://www.radiomasterrc.com/products/tx15",
    "TX5": "https://www.radiomasterrc.com/products/tx12",
    "TX6": "https://www.radiomasterrc.com/products/zorro",
    "TX7": "https://www.radiomasterrc.com/products/pocket",
    "TX8": "https://www.amazon.com/s?k=Jumper+T20+V2+ELRS",
    "TX9": "https://www.amazon.com/s?k=Jumper+T-Pro+V2+ELRS",
    "TX10": "https://www.amazon.com/s?k=BetaFPV+LiteRadio+3+Pro",
    # Video transmitters
    "V1": "https://www.team-blacksheep.com/",
    "V2": "https://www.racedayquads.com/",
    "V3": "https://www.racedayquads.com/",
    "V4": "https://speedybee.com/",
    "V5": "https://www.amazon.com/s?k=Eachine+TX805",
    "V6": "https://www.amazon.com/s?k=Eachine+TX1200",
    "V7": "https://www.racedayquads.com/",
    "V8": "https://www.racedayquads.com/",
    "V9": "https://www.amazon.com/s?k=AKK+FX2+1W",
    "V10": "https://www.getfpv.com/",
    "V11": "https://www.getfpv.com/",
    # Video receivers
    "VRX1": "https://www.amazon.com/s?k=TBS+Fusion+diversity",
    "VRX3": "https://www.amazon.com/s?k=Eachine+ROTG01",
    "VRX4": "https://www.amazon.com/s?k=Eachine+ROTG02",
    "VRX5": "https://www.amazon.com/s?k=Flysight+FSV200",
    "VRX6": "https://www.amazon.com/s?k=Skydroid+150CH+UVC+receiver",
    "VRX7": "https://www.team-blacksheep.com/",
    # USB video captures
    "VC1": "https://www.flyingtech.co.uk/product/usb-c-analog-fpv-video-capture-adapter",
    "VC2": "https://www.aliexpress.com/wholesale?SearchText=CVBS+to+USB+UVC+capture",
    "VC3": "https://www.amazon.com/s?k=AV+to+USB+capture+card+UVC",
    "VC4": "https://www.amazon.com/s?k=EasyCAP+USB+2.0",
    "VC5": "https://www.magewell.com/",
    # Thermal DVRs
    "DVR1": "https://shop.runcam.com/runcam-dvr-mini/",
    "DVR2": "https://www.amazon.com/s?k=Eachine+EV100+Micro+DVR",
    "DVR3": "https://www.amazon.com/s?k=Eachine+ProDVR",
    "DVR4": "https://www.aliexpress.com/wholesale?SearchText=Mini+FPV+DVR+CVBS",
    "DVR5": "https://speedybee.com/",
    "DVR6": "https://www.amazon.com/s?k=Flytron+Micro+DVR",
    "DVR7": "https://www.amazon.com/s?k=ezcap273",
    "DVR8": "https://www.amazon.com/s?k=Zowietek+mega+DVR+III",
    "DVR9": "https://www.amazon.com/s?k=Monster+UVC+Recorder",
    # Telemetry ground links
    "TLM1": "https://www.amazon.com/s?k=Happymodel+ELRS+USB+dongle",
    "TLM2": "https://www.amazon.com/s?k=HGLRC+Hermes+ELRS+USB+dongle",
    "TLM3": "https://www.amazon.com/s?k=RadioMaster+ELRS+USB+dongle",
    "TLM4": "https://www.amazon.com/s?k=BetaFPV+ELRS+nano+dongle",
    "TLM5": "https://www.racedayquads.com/",
}

def update_candidates():
    with open(CANDIDATES_PATH, 'r') as f:
        content = f.read()
    
    changes_made = []
    
    # For each candidate, add purchaseUrl line after the name line and update price
    for cid, url in sorted(PURCHASE_URLS.items(), key=lambda x: len(x[0]), reverse=True):
        # Find the part definition for this candidate
        part_pattern = re.compile(
            r'(  part ' + re.escape(cid) + r' : \w+ \{\n)(.*?)(\n  \})',
            re.DOTALL
        )
        
        match = part_pattern.search(content)
        if not match:
            print(f"  WARNING: Could not find candidate {cid}")
            continue
        
        part_body = match.group(2)
        
        # Check if purchaseUrl already exists
        if ':>> purchaseUrl' in part_body:
            print(f"  SKIP {cid}: purchaseUrl already exists")
            continue
        
        # Add purchaseUrl after name line (insert after the :>> name line)
        # The name line is usually the first :>> attribute
        name_line_match = re.search(r':>> name = "[^"]+";', part_body)
        if name_line_match:
            old_body = part_body
            new_body = part_body[:name_line_match.end()] + f'\n   :>> purchaseUrl = "{url}";' + part_body[name_line_match.end():]
            content = content[:match.start(2)] + new_body + content[match.end(2):]
            changes_made.append(f"  ADD URL {cid}: {url}")
        else:
            print(f"  WARNING: No name line found for {cid}")
    
    # Now apply price corrections
    content_after_urls = content
    
    for cid, (new_price, reason) in sorted(PRICE_CORRECTIONS.items(), key=lambda x: len(x[0]), reverse=True):
        # Find cost_USD line for this candidate
        # We need to be careful to match the right scope
        part_pattern = re.compile(
            r'(  part ' + re.escape(cid) + r' : [\w]+ \{\n)(.*?cost_USD\s*=\s*)([\d.]+)',
            re.DOTALL
        )
        
        match = part_pattern.search(content_after_urls)
        if match:
            old_price = float(match.group(3))
            # Update price
            content_after_urls = content_after_urls[:match.start(3)] + f"{new_price:.2f}" + content_after_urls[match.end(3):]
            changes_made.append(f"  UPDATE PRICE {cid}: ${old_price:.2f} -> ${new_price:.2f} ({reason})")
        else:
            print(f"  WARNING: Could not find cost_USD for {cid}")
    
    # Write updated file
    with open(CANDIDATES_PATH, 'w') as f:
        f.write(content_after_urls)
    
    print(f"\n=== Summary ===")
    for change in changes_made:
        print(change)
    print(f"\nTotal changes: {len(changes_made)}")

if __name__ == "__main__":
    update_candidates()