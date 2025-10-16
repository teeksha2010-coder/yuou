"""
AI Krishi Rakshak Agent
-----------------------
An AI-driven assistant for farmers to:
1. Detect & diagnose pests early using farm images.
2. Recommend natural (eco-friendly) treatments.
3. Guide farmers with local-language instructions (English, Hindi, Kannada).
4. Track effectiveness of treatments.
5. Promote confidence in Natural Farming with measurable results.
"""

import numpy as np
from PIL import Image
import random
import json

# ------------------------------------------------------------
# 1️⃣ DETECT & DIAGNOSE PESTS
# ------------------------------------------------------------
def detect_pests(image_path):
    """Simulated pest detection using color ratios."""
    try:
        img = Image.open(image_path).convert("RGB")
        np_img = np.array(img)
    except Exception as e:
        return {"error": f"Could not open image: {e}"}

    total_pixels = np_img.shape[0] * np_img.shape[1]
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
        pest = "Severe leaf miner / caterpillar infestation"
        life_stage = "advanced"

    return {
        "pest": pest,
        "life_stage": life_stage,
        "confidence": confidence,
        "severity": round(damage_ratio, 3),
        "pixels": {"total": total_pixels, "brown": int(brown), "dark": int(dark)}
    }

# ------------------------------------------------------------
# 2️⃣ RECOMMEND NATURAL TREATMENTS (with translations)
# ------------------------------------------------------------
def recommend_natural_treatment(pest_name, lang="en"):
    """Suggests natural pest control remedies with multilingual support."""
    treatments = {
        "leaf miner": {
            "en": {
                "title": "Neem Oil Spray",
                "details": "Mix 50 ml neem oil + 5 g soap in 1L water; spray every 7 days.",
                "type": "bio-pesticide",
                "notes": "Targets larvae without harming beneficial insects."
            },
            "hi": {
                "title": "नीम तेल छिड़काव",
                "details": "50 मिली नीम तेल + 5 ग्राम साबुन को 1 लीटर पानी में मिलाएं; हर 7 दिन में छिड़काव करें।",
                "type": "जैव कीटनाशक",
                "notes": "लार्वा को निशाना बनाता है और लाभदायक कीड़ों को नुकसान नहीं पहुंचाता।"
            },
            "kn": {
                "title": "ನೀಮ್ ಎಣ್ಣೆ ಸಿಂಪಡಣೆ",
                "details": "50 ಮಿ.ಲೀ. ನೀಮ್ ಎಣ್ಣೆ + 5 ಗ್ರಾಂ ಸಾಬೂನು 1 ಲೀಟರ್ ನೀರಿನಲ್ಲಿ ಮಿಶ್ರಣಿಸಿ; ಪ್ರತಿ 7 ದಿನಗಳಿಗೊಮ್ಮೆ ಸಿಂಪಡಿಸಿ.",
                "type": "ಜೈವ ಕೀಟನಾಶಕ",
                "notes": "ಉಪಯುಕ್ತ ಕೀಟಗಳಿಗೆ ಹಾನಿ ಮಾಡದೆ ಲಾರ್ವಾಗಳನ್ನು ಗುರಿಯಾಗಿಸುತ್ತದೆ."
            }
        },
        "caterpillar": {
            "en": {
                "title": "Bt Spray (Bacillus thuringiensis)",
                "details": "Dilute 2g Bt powder per liter; apply in evening hours.",
                "type": "microbial pesticide",
                "notes": "Highly specific and environmentally safe."
            },
            "hi": {
                "title": "बीटी छिड़काव (बैसिलस थ्यूरिनजेंसिस)",
                "details": "प्रति लीटर 2 ग्राम बीटी पाउडर घोलें; शाम के समय छिड़काव करें।",
                "type": "सूक्ष्मजीव कीटनाशक",
                "notes": "अत्यधिक विशिष्ट और पर्यावरण के लिए सुरक्षित।"
            },
            "kn": {
                "title": "ಬಿ.ಟಿ. ಸಿಂಪಡಣೆ (Bacillus thuringiensis)",
                "details": "ಪ್ರತಿ ಲೀಟರ್‌ಗೆ 2 ಗ್ರಾಂ ಬಿ.ಟಿ. ಪುಡಿ ಕರಗಿಸಿ; ಸಂಜೆ ಸಮಯದಲ್ಲಿ ಅನ್ವಯಿಸಿ.",
                "type": "ಸೂಕ್ಷ್ಮಾಣು ಕೀಟನಾಶಕ",
                "notes": "ಬಹಳ ನಿಖರವಾದ ಮತ್ತು ಪರಿಸರಕ್ಕೆ ಸುರಕ್ಷಿತ."
            }
        },
        "default": {
            "en": {
                "title": "Garlic-Chili Spray",
                "details": "Crush 50g garlic + 20g green chili in 1L water, filter & spray.",
                "type": "natural repellent",
                "notes": "Effective against early-stage chewing pests."
            },
            "hi": {
                "title": "लहसुन-मिर्च छिड़काव",
                "details": "50 ग्राम लहसुन और 20 ग्राम हरी मिर्च को 1 लीटर पानी में पीसकर छानें और छिड़कें।",
                "type": "प्राकृतिक कीट प्रतिरोधक",
                "notes": "प्रारंभिक चरण के कीटों के खिलाफ प्रभावी।"
            },
            "kn": {
                "title": "ಬೆಳ್ಳುಳ್ಳಿ-ಮೆಣಸಿನ ಸಿಂಪಡಣೆ",
                "details": "50 ಗ್ರಾಂ ಬೆಳ್ಳುಳ್ಳಿ ಮತ್ತು 20 ಗ್ರಾಂ ಹಸಿಮೆಣಸನ್ನು 1 ಲೀಟರ್ ನೀರಿನಲ್ಲಿ ರುಬ್ಬಿ ಶೋಧಿಸಿ ಸಿಂಪಡಿಸಿ.",
                "type": "ಸಹಜ ಕೀಟ ಪ್ರತಿರೋಧಕ",
                "notes": "ಆರಂಭಿಕ ಹಂತದ ಕೀಟಗಳ ವಿರುದ್ಧ ಪರಿಣಾಮಕಾರಿ."
            }
        }
    }

    if "leaf miner" in pest_name.lower():
        return treatments["leaf miner"].get(lang, treatments["leaf miner"]["en"])
    elif "caterpillar" in pest_name.lower():
        return treatments["caterpillar"].get(lang, treatments["caterpillar"]["en"])
    else:
        return treatments["default"].get(lang, treatments["default"]["en"])

# ------------------------------------------------------------
# 3️⃣ GUIDE FARMER IN LOCAL LANGUAGE
# ------------------------------------------------------------
def guide_farmer(treatment):
    """Formats the treatment message clearly for farmers."""
    return f"{treatment['title']} — {treatment['details']} (Note: {treatment['notes']})"

# ------------------------------------------------------------
# 4️⃣ TRACK EFFECTIVENESS OF TREATMENT
# ------------------------------------------------------------
def track_effectiveness(before, after):
    """Quantifies pest reduction & yield improvement."""
    reduction = max(0, before["severity"] - after["severity"])
    yield_change = (reduction * 0.8 - before["severity"] * 0.5) * 100
    return {
        "severity_reduction": round(reduction, 3),
        "estimated_yield_change_%": round(yield_change, 2)
    }

# ------------------------------------------------------------
# 5️⃣ MAIN EXECUTION FUNCTION
# ------------------------------------------------------------
def krishi_rakshak(image_before, image_after=None, lang="en"):
    diagnosis_before = detect_pests(image_before)
    if "error" in diagnosis_before:
        return diagnosis_before

    treatment = recommend_natural_treatment(diagnosis_before["pest"], lang)
    guide = guide_farmer(treatment)

    if image_after:
        diagnosis_after = detect_pests(image_after)
        tracking = track_effectiveness(diagnosis_before, diagnosis_after)
    else:
        diagnosis_after = None
        tracking = None

    return {
        "diagnosis": diagnosis_before,
        "treatment": treatment,
        "guidance": guide,
        "tracking": tracking
    }

# ------------------------------------------------------------
# 6️⃣ DEMO / TEST EXECUTION
# ------------------------------------------------------------
if __name__ == "__main__":
    print("🌿 AI Krishi Rakshak Agent Started...\n")
    before_path = input("Enter path to 'before treatment' farm image: ").strip()
    after_path = input("Enter path to 'after treatment' image (or press Enter to skip): ").strip()
    lang = input("Enter language (en / hi / kn): ").strip().lower() or "en"

    after_path = after_path if after_path else None
    result = krishi_rakshak(before_path, after_path, lang)

    print("\n🧾 AI Krishi Rakshak Report:")
    print(json.dumps(result, indent=4, ensure_ascii=False))