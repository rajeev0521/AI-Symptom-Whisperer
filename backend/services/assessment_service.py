class AssessmentService:
    """
    Handles mental health assessments (e.g., PHQ-9, GAD-7).
    """
    def process_assessment(self, assessment_type: str, answers: list) -> dict:
        if assessment_type == "phq9":
            score = sum(answers)
            severity = self._phq9_severity(score)
            return {"score": score, "severity": severity}
        elif assessment_type == "gad7":
            score = sum(answers)
            severity = self._gad7_severity(score)
            return {"score": score, "severity": severity}
        else:
            return {"error": "Unknown assessment type."}

    def _phq9_severity(self, score: int) -> str:
        if score < 5: return "Minimal"
        if score < 10: return "Mild"
        if score < 15: return "Moderate"
        if score < 20: return "Moderately Severe"
        return "Severe"

    def _gad7_severity(self, score: int) -> str:
        if score < 5: return "Minimal"
        if score < 10: return "Mild"
        if score < 15: return "Moderate"
        return "Severe"
