import re

RE_FAMX_BODY = re.compile(
    r"received\s*\*?₹\*?\s*([0-9]+(?:\.[0-9]+)?)\*?\s*from\s*\*?([A-Z ]+)\*?.*?transaction id\s*([A-Z0-9]+)",
    re.IGNORECASE | re.DOTALL
)

def extract_amount_and_payer(text):
    t = text.replace("\xa0", " ").replace("\n", " ").replace("\r", " ")
    t = re.sub(r"\s+", " ", t).strip()
    match = RE_FAMX_BODY.search(t)
    if match:
        amount = float(match.group(1))
        payer = match.group(2).strip().title()
        txnid = match.group(3).strip()
        return amount, payer, txnid
    return None, None, None
