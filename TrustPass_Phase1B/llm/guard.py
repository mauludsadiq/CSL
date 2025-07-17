# trustpass/llm/guard.py

class Guard:
    """Base LLM guardrail for drift detection and correction."""
    def __init__(self):
        pass

    def evaluate(self, text: str) -> tuple[float, list[str]]:
        """Mock drift evaluation."""
        drift_score = 0.5
        violations = ["UNSOURCED_CLAIM"]
        return drift_score, violations

    def correct(self, text: str) -> str:
        """Simple mock correction."""
        return text.replace("refused treatment", "discussed treatment options")
