"""
AI Krishi Rakshak Agent
-----------------------
An AI-driven assistant for farmers to:
1. Detect & diagnose pests early using farm images.
2. Recommend natural (eco-friendly) treatments.
3. Guide farmers with local-language instructions.
4. Track effectiveness of treatments.
5. Promote confidence in Natural Farming with measurable results.
"""

import numpy as np
from PIL import Image
import random
import json
import os


# ------------------------------------------------------------
# 1️⃣ DETECT & DIAGNOSE PESTS
# ------------------------------------------------------------
def detect_pests(image_path):
    """
    Simulated pest detection using color ratios.
    Real-world version: Replace with a trained CNN/TFLite pest classifier.
    """
    if not os.path.exists(image_path):
        return {"error": f"Image not found: {image_path}"}

    try:
        img = Image.open(image_path).convert("RGB")
        np_img = np.array(img)
    except Exception as e:
        return {"error": f"Could not open image: {e}"}

    if np_img.ndim != 3 or np_img.shape[2] != 3:
        return {"error": "Invalid image format. Please use a color image (RGB)."}

    total_pixels = np_img.shape[0] * np_img.shape[1]

    # Approximate color-based pest damage estimation
    brown = np.sum((np_img[:, :, 0] > 100) & (np_img[:, :, 1] < 80) & (np_img[:, :, 2] < 60))
    dark = np.sum(np.mean(np_img, axis=2) < 50)

    damage_ratio = (brown + dark) / total_pixels
    confidence = round(random.uniform(0.5, 0.9), 2)

    if damage_ratio < 0.05:
        pest = "No significant pest"
        life_stage = "N/A"
    elif damage_ratio < 0.15:
        pest = "Early leaf miner or minor chewing pest"
        life_stage = "early"
    else:
        pest = "Severe leaf miner or caterpillar infestation"
        life_stage = "advanced"

    return {
        "pest": pest,
        "life_stage": life_stage,
        "confidence": confidence,
        "severity": round(damage_ratio, 3),
        "pixels": {
            "total": int(total_pixels),
            "brown": int(brown),
            "dark": int(dark)
        }
    }


# ------------------------------------------------------------
# 2️⃣ RECOMMEND NATURAL TREATMENTS
# ------------------------------------------------------------
def recommend_natural_treatment(pest_name):
    """
    Suggests natural / bio-based pest control treatments.
    Extendable with more pest types and local crops.
    """
    treatments = {
        "leaf miner": {
            "title": "Neem Oil Spray",
            "details": "Mix 50 ml neem oil + 5 g mild soap in 1L water; spray every 7 days.",
            "type": "bio-pesticide",
            "notes": "Targets larvae without harming beneficial insects."
        },
        "caterpillar": {
            "title": "Bt Spray (Bacillus thuringiensis)",
            "details": "Dilute 2 g Bt powder per liter; apply during evening hours.",
            "type": "microbial pesticide",
            "notes": "Highly specific and environmentally safe."
        },
        "default": {
            "title": "Garlic-Chili Spray",
            "details": "Crush 50 g garlic + 20 g green chili in 1L water, filter & spray.",
            "type": "natural repellent",
            "notes": "Effective against early-stage chewing pests."
        }
    }

    pest_name_lower = pest_name.lower()
    if "leaf miner" in pest_name_lower:
        return treatments["leaf miner"]
    elif "caterpillar" in pest_name_lower:
        return treatments["caterpillar"]
    else:
        return treatments["default"]


# ------------------------------------------------------------
# 3️⃣ GUIDE FARMERS IN LOCAL LANGUAGE
# ------------------------------------------------------------
def guide_farmer(treatment, lang="en"):
    """
    Provides farmer-friendly instructions in multiple languages.
    Extendable to include voice generation (TTS).
    """
    guides = {
        "en": f"Apply {treatment['title']} — {treatment['details']}. Note: {treatment['notes']}",
        "hi": f"{treatment['title']} लगाएं — {treatment['details']}. ध्यान दें: {treatment['notes']}",
        "kn": f"{treatment['title']} ಅನ್ವಯಿಸಿ — {treatment['details']}. ಗಮನಿಸಿ: {treatment['notes']}"
    }
    return guides.get(lang, guides["en"])


# ------------------------------------------------------------
# 4️⃣ TRACK EFFECTIVENESS OF TREATMENT
# ------------------------------------------------------------
def track_effectiveness(before, after):
    """
    Quantifies pest reduction & estimates yield improvement.
    """
    if not before or not after:
        return {"error": "Both before and after images are required for tracking."}

    reduction = max(0, before["severity"] - after["severity"])
    yield_change = (reduction * 0.8 - before["severity"] * 0.5) * 100

    return {
        "severity_reduction": round(reduction, 3),
        "estimated_yield_change_%": round(yield_change, 2)
    }


# ------------------------------------------------------------
# 5️⃣ CORE AGENT FUNCTION
# ------------------------------------------------------------
def krishi_rakshak(image_before, image_after=None, lang="en"):
    """
    Core AI agent function — ties together all features.
    """
    diagnosis_before = detect_pests(image_before)
    if "error" in diagnosis_before:
        return diagnosis_before

    treatment = recommend_natural_treatment(diagnosis_before["pest"])
    guidance = guide_farmer(treatment, lang)

    diagnosis_after = None
    tracking = None
    if image_after:
        diagnosis_after = detect_pests(image_after)
        if "error" not in diagnosis_after:
            tracking = track_effectiveness(diagnosis_before, diagnosis_after)

    return {
        "diagnosis_before": diagnosis_before,
        "treatment": treatment,
        "guidance": guidance,
        "diagnosis_after": diagnosis_after,
        "tracking": tracking
    }


# ------------------------------------------------------------
# 6️⃣ MAIN FUNCTION
# ------------------------------------------------------------
def main():
    print("🌿 AI Krishi Rakshak Agent Started...\n")

    before_path = input("Enter path to 'before treatment' farm image: ").strip()
    after_path = input("Enter path to 'after treatment' image (or press Enter to skip): ").strip()
    lang = input("Enter language (en / hi / kn): ").strip().lower() or "en"

    after_path = after_path if after_path else None
    result = krishi_rakshak(before_path, after_path, lang)

    print("\n🧾 AI Krishi Rakshak Report:")
    print(json.dumps(result, indent=4, ensure_ascii=False))


# ------------------------------------------------------------
# 7️⃣ RUN MAIN
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
