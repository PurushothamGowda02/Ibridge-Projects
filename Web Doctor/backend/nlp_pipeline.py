from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from medical_triage import MEDICAL_TRIAGE_DATASET, RuleBasedTriageEngine


class HybridClinicalNLPPipeline:
    ML_CONFIDENCE_THRESHOLD = 0.68

    def __init__(self, artifact_path: str = "ml/artifacts/triage_tfidf.joblib"):
        self.rule_engine = RuleBasedTriageEngine(MEDICAL_TRIAGE_DATASET)
        self.artifact_path = Path(__file__).parent / artifact_path
        self.ml_bundle = self._load_ml_artifact()

    def _load_ml_artifact(self):
        if not self.artifact_path.exists():
            return None

        try:
            import joblib
        except Exception:
            return None

        try:
            return joblib.load(self.artifact_path)
        except Exception:
            return None

    def _ml_predict(self, normalized_symptoms: str) -> Optional[Dict[str, object]]:
        if not self.ml_bundle:
            return None

        model = self.ml_bundle.get("model")
        vectorizer = self.ml_bundle.get("vectorizer")
        labels = self.ml_bundle.get("labels", [])

        if not model or not vectorizer or not labels:
            return None

        vec = vectorizer.transform([normalized_symptoms])
        pred_idx = int(model.predict(vec)[0])
        confidence = None
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(vec)[0]
            confidence = float(proba[pred_idx])

        if pred_idx < 0 or pred_idx >= len(labels):
            return None

        condition = labels[pred_idx]
        mapped = self.rule_engine.profile_from_condition(condition)
        if mapped is None:
            return None

        mapped["model_source"] = "Fine-tuned clinical classifier (artifact)"
        mapped["confidence"] = round(confidence, 3) if confidence is not None else None
        return mapped

    def analyze(self, symptoms: str, language: str = "en") -> Dict[str, object]:
        normalized = self.rule_engine.normalize_multilingual_symptoms(symptoms, language)

        rule_output, rule_confidence = self.rule_engine.analyze_rule_based(normalized)
        ml_output = self._ml_predict(normalized)

        ml_confidence = ml_output.get("confidence") if ml_output else None
        should_use_ml = (
            ml_output is not None
            and ml_confidence is not None
            and ml_confidence >= self.ML_CONFIDENCE_THRESHOLD
        )

        # Safety guard: if rule engine finds emergency, never downgrade from it.
        if should_use_ml and rule_output.get("severity") != "Emergency":
            ml_output["input_language"] = language
            ml_output["normalized_symptoms"] = normalized
            return ml_output

        rule_output.update(
            {
                "model_source": "Rule-based medical triage dataset",
                "confidence": rule_confidence,
                "input_language": language,
                "normalized_symptoms": normalized,
            }
        )
        return rule_output

    def model_info(self) -> Dict[str, object]:
        info = self.rule_engine.model_info()
        info["type"] = (
            "Hybrid clinical NLP + rules (ML artifact active)"
            if self.ml_bundle
            else "Hybrid clinical NLP + rules (rule engine active, ML artifact not loaded)"
        )
        return info
