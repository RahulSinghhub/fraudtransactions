from dataclasses import dataclass
from account_profile import AccountProfile
from transaction import Transaction
from rules import ALL_RULES

@dataclass
class ScoreResult:
    txn_id : str
    score : int
    verdict : str
    reasons : list[str]

class FraudEngine:

    def __init__(self):
        self.profile = AccountProfile()

    def score(self, txn: Transaction, now = None):
        if now is None:
            now = txn.timestamp
        reasons = []
        score = 0
        
        for rule in ALL_RULES:
            ans = rule(txn, self.profile, now)

            if ans is not None:
                reason, weight = ans
                reasons.append(reason)
                score += weight

        verdict = "BLOCK" if score >= 60 else "REVIEW" if score >= 30 else "APPROVE"

        self.profile.record(txn)

        return ScoreResult(txn_id = txn.txn_id, score = score, verdict = verdict, reasons = reasons)