from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class ConditionProfile:
    condition: str
    specialist: str
    severity: str
    recommendation: str
    first_aid: List[str]
    precaution: List[str]
    symptom_terms: List[str]


def _normalize_tokens(text: str) -> List[str]:
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
    return [token for token in cleaned.split() if len(token) > 2]


HINDI_TO_ENGLISH_SYMPTOM_MAP = {
    "bukhar": "fever",
    "khansi": "cough",
    "sar dard": "headache",
    "pet dard": "stomach pain",
    "ulti": "vomiting",
    "saans": "breath",
    "saans lene mein dikkat": "breathing difficulty",
    "chakkar": "dizziness",
    "dast": "diarrhea",
    "thakan": "fatigue",
    "kamzori": "weakness",
    "sardi": "cold",
    "gale mein dard": "sore throat",
    "bukhar aur khansi": "fever cough",
    "seene mein dard": "chest pain",
    "sar par chot": "head injury",
    "sir par chot": "head injury",
    "sar mein chot": "head injury",
    "sir mein chot": "head injury",
    "सांस": "breath",
    "बुखार": "fever",
    "खांसी": "cough",
    "सिर दर्द": "headache",
    "पेट दर्द": "stomach pain",
    "उल्टी": "vomiting",
    "दस्त": "diarrhea",
    "सिर में चोट": "head injury",
    "सिर पर चोट": "head injury",
    "बेहोश": "unconscious",
    "चोट": "injury",
    "गिर गया": "fall",
    "सर पर चोट": "head injury",
}


MEDICAL_TRIAGE_DATASET: List[ConditionProfile] = [
    ConditionProfile(
        condition="Possible Cardiac Emergency",
        specialist="Emergency Medicine / Cardiology",
        severity="Emergency",
        recommendation="Call emergency services immediately. Chest pain with breathing difficulty can be life threatening.",
        first_aid=[
            "Call emergency services now.",
            "Keep the person seated and calm.",
            "Loosen tight clothes around the neck and chest.",
            "If conscious and not allergic, chew one aspirin tablet while waiting for help.",
        ],
        precaution=[
            "Do not allow walking or exertion.",
            "Do not delay emergency care.",
            "Do not give food or alcohol.",
        ],
        symptom_terms=["chest pain", "chest tightness", "left arm pain", "jaw pain", "sweating", "breathlessness", "heart"],
    ),
    ConditionProfile(
        condition="Respiratory Distress",
        specialist="Emergency Medicine / Pulmonology",
        severity="Emergency",
        recommendation="Call emergency services right away. Breathing problems can become critical quickly.",
        first_aid=[
            "Sit upright and lean slightly forward.",
            "Use prescribed inhaler if available.",
            "Keep surroundings ventilated.",
        ],
        precaution=[
            "Do not lie flat.",
            "Do not leave the person alone.",
            "Do not force food or water.",
        ],
        symptom_terms=["shortness of breath", "cannot breathe", "wheezing", "choking", "breathing difficulty", "oxygen"],
    ),
    ConditionProfile(
        condition="Upper Respiratory Viral Infection",
        specialist="General Physician",
        severity="Moderate",
        recommendation="Most cases improve in a few days with hydration and rest. Seek medical care if fever remains high or symptoms worsen.",
        first_aid=[
            "Drink fluids and oral rehydration solution.",
            "Take adequate rest.",
            "Use paracetamol for fever as per label instructions.",
            "Use warm steam or saline rinse for congestion.",
        ],
        precaution=[
            "Avoid unnecessary antibiotics without prescription.",
            "Isolate if fever and cough are present.",
            "Get medical review if symptoms last beyond 3 days.",
        ],
        symptom_terms=["fever", "cough", "sore throat", "runny nose", "body ache", "cold", "chills", "fatigue"],
    ),
    ConditionProfile(
        condition="Acute Gastrointestinal Illness",
        specialist="General Physician / Gastroenterology",
        severity="Moderate",
        recommendation="Hydration is the first priority. Seek urgent care if blood in stool, persistent vomiting, or dehydration appears.",
        first_aid=[
            "Take small frequent sips of ORS.",
            "Start bland food after vomiting settles.",
            "Rest and monitor urine output.",
        ],
        precaution=[
            "Avoid oily and spicy foods.",
            "Avoid anti-diarrheal drugs without physician advice in severe infection.",
            "Seek care for persistent high fever or blood in stool.",
        ],
        symptom_terms=["diarrhea", "vomiting", "nausea", "stomach pain", "abdominal pain", "food poisoning", "loose motion"],
    ),
    ConditionProfile(
        condition="Head Injury / Concussion Risk",
        specialist="Emergency Medicine / Neurology",
        severity="Emergency",
        recommendation="Head injury can be dangerous even when symptoms seem mild at first. Seek urgent emergency evaluation, especially if there is vomiting, confusion, fainting, seizure, bleeding, or severe headache.",
        first_aid=[
            "Keep the person still and monitor consciousness.",
            "Apply a cold pack wrapped in cloth to swollen areas.",
            "If bleeding, apply gentle pressure with clean cloth.",
            "If unconscious or vomiting repeatedly, call emergency services immediately.",
        ],
        precaution=[
            "Do not let the person sleep without observation in the first few hours.",
            "Do not give alcohol or sedative medications.",
            "Do not ignore confusion, unequal pupils, repeated vomiting, or seizure.",
            "Do not move the neck aggressively if fall or accident involved.",
        ],
        symptom_terms=[
            "head injury",
            "head trauma",
            "hit head",
            "concussion",
            "fall and hit head",
            "bleeding from head",
            "loss of consciousness",
            "unconscious after injury",
            "vomiting after head injury",
            "drowsy after hit",
            "confusion after injury",
            "seizure after head injury",
            "brain injury",
        ],
    ),
    ConditionProfile(
        condition="Tension Headache or Migraine",
        specialist="General Physician / Neurology",
        severity="Low",
        recommendation="Rest in a calm environment and hydrate. Seek urgent care for sudden worst headache or neurological symptoms.",
        first_aid=[
            "Rest in a dark and quiet room.",
            "Use a cold or warm compress based on comfort.",
            "Hydrate and avoid bright screens.",
        ],
        precaution=[
            "Do not ignore severe sudden headache.",
            "Avoid sleep deprivation and missed meals.",
        ],
        symptom_terms=["headache", "migraine", "throbbing", "sensitivity to light", "head pain", "nausea with headache"],
    ),
    ConditionProfile(
        condition="Skin Allergy or Irritation",
        specialist="Dermatology",
        severity="Low",
        recommendation="Mild allergy often improves with avoidance of trigger and antihistamine. Escalate quickly if swelling or breathing difficulty occurs.",
        first_aid=[
            "Wash exposed skin with clean water.",
            "Use cool compress on itchy area.",
            "Take over-the-counter antihistamine if suitable.",
        ],
        precaution=[
            "Do not scratch affected skin.",
            "Do not continue contact with likely allergen.",
            "Seek emergency help for throat swelling or breathing difficulty.",
        ],
        symptom_terms=["rash", "itching", "hives", "allergy", "skin redness", "irritation"],
    ),
    ConditionProfile(
        condition="Musculoskeletal Injury (Sprain or Strain)",
        specialist="Orthopedics",
        severity="Moderate",
        recommendation="Use RICE care in first 24 to 48 hours and get imaging if severe pain, deformity, or inability to bear weight.",
        first_aid=[
            "Rest the injured area.",
            "Apply ice with cloth barrier for 15 to 20 minutes.",
            "Use compression bandage and elevate limb.",
        ],
        precaution=[
            "Do not force movement in severe pain.",
            "Do not apply direct heat immediately after injury.",
        ],
        symptom_terms=["ankle twist", "sprain", "swelling", "joint pain", "muscle pull", "injury", "strain"],
    ),
]


class RuleBasedTriageEngine:
    def __init__(self, profiles: List[ConditionProfile]):
        self.profiles = profiles
        self.profile_by_condition = {p.condition: p for p in profiles}
        self.fallback = {
            "condition": "General Mild Illness",
            "specialist": "General Physician",
            "severity": "Low",
            "recommendation": "Current symptoms appear non-specific. Rest, hydrate, and monitor. Seek medical care if symptoms persist or worsen.",
            "first_aid": [
                "Take adequate fluids and rest.",
                "Track temperature and symptom changes.",
                "Avoid self-medication with strong drugs.",
            ],
            "precaution": [
                "Seek professional care if symptoms continue beyond 48 hours.",
                "Go to emergency care for severe breathlessness, chest pain, or confusion.",
            ],
        }

    def normalize_multilingual_symptoms(self, symptoms: str, language: str) -> str:
        normalized = symptoms.lower().strip()
        if language.lower() in {"hi", "hindi", "hinglish"}:
            for hindi_term, english_term in HINDI_TO_ENGLISH_SYMPTOM_MAP.items():
                normalized = normalized.replace(hindi_term, english_term)
        return normalized

    def _profile_to_output(self, profile: ConditionProfile) -> Dict[str, object]:
        return {
            "condition": profile.condition,
            "specialist": profile.specialist,
            "severity": profile.severity,
            "recommendation": profile.recommendation,
            "first_aid": profile.first_aid,
            "precaution": profile.precaution,
        }

    def analyze_rule_based(self, normalized_symptoms: str) -> Tuple[Dict[str, object], float]:
        if not normalized_symptoms:
            return self.fallback, 0.1

        input_tokens = set(_normalize_tokens(normalized_symptoms))

        best_profile: Optional[ConditionProfile] = None
        best_score = 0.0

        for profile in self.profiles:
            score = 0.0
            for phrase in profile.symptom_terms:
                phrase_tokens = _normalize_tokens(phrase)
                if phrase in normalized_symptoms:
                    score += 3.0
                    if profile.severity == "Emergency":
                        # Give higher priority to direct emergency phrase matches.
                        score += 4.0
                token_overlap = len(input_tokens.intersection(phrase_tokens))
                score += token_overlap * 1.0
            if score > best_score:
                best_score = score
                best_profile = profile

        if best_profile is None:
            return self.fallback, 0.1

        confidence = min(0.98, 0.35 + (best_score / 12.0))
        return self._profile_to_output(best_profile), round(confidence, 3)

    def profile_from_condition(self, condition: str) -> Optional[Dict[str, object]]:
        profile = self.profile_by_condition.get(condition)
        if profile is None:
            return None
        return self._profile_to_output(profile)

    def model_info(self) -> Dict[str, object]:
        return {
            "name": "Clinical Triage Engine v2",
            "type": "Hybrid clinical NLP + rules",
            "clinical_scope": "Common non-surgical primary care symptoms with emergency escalation patterns",
            "datasets": [
                "MIMIC-style symptom-note JSONL schema for retraining",
                "Curated emergency red-flag patterns",
                "Domain symptom-to-condition mapping dataset",
            ],
            "intended_use": "First-line guidance for low-cost early decision support before clinical consultation",
            "limitations": "Not a diagnostic replacement. Does not prescribe medicines or handle rare disease diagnosis.",
            "emergency_notice": "For severe chest pain, breathing difficulty, stroke signs, or unconsciousness, contact emergency services immediately.",
            "multilingual_support": ["English", "Hindi", "Hinglish"],
        }
