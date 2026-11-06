from __future__ import annotations

from datetime import date
from pathlib import Path
import re

import pandas as pd
import streamlit as st


st.set_page_config(page_title="Udyam Digital | Accel Business", page_icon="📶", layout="wide")

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "6ae1873397bc1_digital" / "YTL_TrackA_Udyam_Digital_Data"
DOCS = DATA / "kyc_documents"
TODAY = date(2026, 7, 15)  # fixed reference date specified by the challenge data pack


@st.cache_data
def load_data():
    return (
        pd.read_csv(DATA / "product_catalogue.csv").fillna(""),
        pd.read_csv(DATA / "smb_leads.csv"),
        pd.read_csv(DATA / "mock_gstin_registry.csv", dtype={"gstin": str}),
        pd.read_csv(DATA / "mock_udyam_registry.csv", dtype={"udyam_number": str}),
    )


try:
    PRODUCTS, LEADS, GST, UDYAM = load_data()
except Exception as exc:  # friendly setup error when launched outside the supplied folder
    st.error(f"Could not load the supplied challenge data: {exc}")
    st.stop()


TEXT = {
    "English": {
        "title": "Project Udyam Digital",
        "subtitle": "One simple journey to the right business bundle.",
        "guided": "Guided advisor · Catalogue-grounded demo · No external AI calls",
        "business": "Business profile",
        "type": "Business type",
        "tier": "City tier",
        "employees": "Employees",
        "sites": "Sites",
        "internet": "Fibre available at the site?",
        "gst": "Business has GSTIN?",
        "lang": "Preferred language",
        "recommend": "Recommend my bundle",
        "quote": "Your transparent quote",
        "monthly": "Monthly total",
        "setup": "One-time setup",
        "consent": "I consent to using these details only to demonstrate KYC validation in this synthetic prototype.",
        "kyc": "Smart KYC",
        "tracker": "Order tracker",
        "insights": "Business evidence",
        "review": "Manual review needed",
        "verified": "Registry match found",
        "privacy": "Your upload stays in this browser session and is not saved by this demo.",
    },
    "हिन्दी": {
        "title": "प्रोजेक्ट उद्यम डिजिटल",
        "subtitle": "आपके व्यवसाय के लिए सही कनेक्टिविटी और सेवाएँ, एक सरल प्रक्रिया में।",
        "guided": "गाइडेड सलाहकार · कैटलॉग आधारित डेमो · बाहरी AI सेवा का उपयोग नहीं",
        "business": "व्यवसाय की जानकारी",
        "type": "व्यवसाय का प्रकार",
        "tier": "शहर का स्तर",
        "employees": "कर्मचारी",
        "sites": "स्थान",
        "internet": "क्या यहाँ फाइबर उपलब्ध है?",
        "gst": "क्या GSTIN है?",
        "lang": "पसंदीदा भाषा",
        "recommend": "मेरे लिए बंडल सुझाएँ",
        "quote": "आपका स्पष्ट कोटेशन",
        "monthly": "मासिक कुल",
        "setup": "एक बार का सेटअप",
        "consent": "मैं इस सिंथेटिक प्रोटोटाइप में KYC जाँच दिखाने के लिए इन विवरणों के उपयोग की सहमति देता/देती हूँ।",
        "kyc": "स्मार्ट KYC",
        "tracker": "ऑर्डर ट्रैकर",
        "insights": "व्यावसायिक आँकड़े",
        "review": "मानवीय समीक्षा आवश्यक",
        "verified": "रजिस्ट्री रिकॉर्ड मिला",
        "privacy": "आपकी फ़ाइल इसी ब्राउज़र सत्र में रहती है; डेमो इसे सेव नहीं करता।",
    },
}


def money(value) -> str:
    return f"₹{float(value):,.0f}"


def norm(value: str) -> str:
    value = re.sub(r"[^a-z0-9 ]", " ", str(value).lower())
    ignored = {"prop", "proprietor", "proprietorship", "pvt", "private", "limited", "ltd", "llp"}
    return " ".join(part for part in value.split() if part not in ignored)


def product_row(pid: str):
    rows = PRODUCTS[PRODUCTS.product_id == pid]
    return None if rows.empty else rows.iloc[0]


def is_eligible(p, profile: dict) -> tuple[bool, str]:
    tiers = str(p.available_city_tiers).split(";")
    if str(profile["tier"]) not in tiers:
        return False, "Not offered in this city tier"
    if int(profile["employees"]) < int(p.min_employees):
        return False, f"Needs {int(p.min_employees)}+ employees"
    if int(profile["sites"]) < int(p.min_sites):
        return False, f"Needs {int(p.min_sites)}+ sites"
    if p.requires_gstin == "Y" and not profile["gst"]:
        return False, "Requires GSTIN"
    target = [x.strip() for x in str(p.target_segments).split(";") if x.strip()]
    if profile["segment_code"] not in target:
        return False, "Not designed for this segment"
    return True, "Eligible"


def quantities(profile: dict) -> dict[str, int]:
    return {
        "P02": int(profile["sites"]),
        "P09": int(profile["sites"]),
        "P10": int(profile["sites"]),
        "P16": min(5, int(profile["employees"])),
        "P20": min(5, int(profile["employees"])),
        "P07": min(3, int(profile["employees"])),
    }


def suggested_ids(profile: dict) -> list[str]:
    seg = profile["segment_code"]
    fiber = "P01" if seg == "micro" else "P02"
    base = fiber if profile["fiber"] else "P04"
    ids = [base]
    if seg == "micro":
        ids += ["P07", "P19"]
    elif seg == "prof":
        ids += ["P16", "P20"]
        if profile["gst"]:
            ids.append("P12")
    elif seg == "multi":
        ids += ["P07", "P09"]
        if profile["gst"] and profile["employees"] >= 10 and profile["sites"] >= 3:
            ids.append("P10")
    else:  # mfg
        ids = ["P05", "P07"] if profile["gst"] and profile["employees"] >= 10 else ["P04", "P07"]
        if profile["gst"]:
            ids.append("P24")
    valid = []
    for pid in ids:
        p = product_row(pid)
        if p is not None and is_eligible(p, profile)[0]:
            valid.append(pid)
    return list(dict.fromkeys(valid))


def render_quote(ids: list[str], profile: dict):
    q = quantities(profile)
    rows = []
    for pid in ids:
        p = product_row(pid)
        if p is None:
            continue
        quantity = q.get(pid, int(profile["sites"]) if p.unit == "per site" else 1)
        rows.append({
            "Product": p.product_name,
            "Qty": quantity,
            "Monthly": float(p.price_min_inr_per_month) * quantity,
            "Setup": float(p.one_time_setup_inr) * quantity,
            "Term": f"{int(p.min_contract_months)} months",
        })
    if not rows:
        return pd.DataFrame(), 0, 0, 0
    frame = pd.DataFrame(rows)
    return frame, frame.Monthly.sum(), frame.Setup.sum(), max(int(product_row(pid).min_contract_months) for pid in ids)


import importlib
import frontend

importlib.reload(frontend)
frontend.render_frontend(PRODUCTS, LEADS, GST, UDYAM, DOCS, money, norm, product_row, is_eligible, quantities, suggested_ids, render_quote)

