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


language = st.sidebar.selectbox("Language / भाषा", ["English", "हिन्दी"], index=0)
t = TEXT[language]
st.sidebar.markdown("### Airtel SYNC · Digital Track")
st.sidebar.caption(t["guided"])
page = st.sidebar.radio("Journey", ["Advisor & quote", t["kyc"], t["tracker"], t["insights"]])
st.title(t["title"])
st.caption(t["subtitle"])


if page == "Advisor & quote":
    st.subheader(t["business"])
    types = {
        "Kirana / retail / services": ("Micro retail & services", "micro"),
        "Clinic / CA / coaching": ("Professional offices", "prof"),
        "Restaurant / multi-site retailer": ("Small multi-site businesses", "multi"),
        "Small manufacturer": ("Small manufacturers", "mfg"),
    }
    left, right = st.columns(2)
    with left:
        kind = st.selectbox(t["type"], list(types))
        city_tier = st.selectbox(t["tier"], [1, 2], format_func=lambda n: f"Tier {n}")
        employees = st.number_input(t["employees"], 1, 500, 3)
        sites = st.number_input(t["sites"], 1, 100, 1)
    with right:
        fiber = st.toggle(t["internet"], value=True)
        has_gst = st.toggle(t["gst"], value=True)
        language_pref = st.selectbox(t["lang"], ["Hindi", "English", "Marathi", "Telugu", "Tamil", "Kannada", "Gujarati", "Bengali", "Punjabi", "Malayalam"])
        interests = st.multiselect("What would help most?", ["Reliable internet", "Business SIMs", "Customer messaging", "Billing/POS", "Cloud and security"], default=["Reliable internet"])

    segment, code = types[kind]
    profile = {"segment": segment, "segment_code": code, "tier": city_tier, "employees": int(employees), "sites": int(sites), "fiber": fiber, "gst": has_gst}
    base_ids = suggested_ids(profile)
    if st.button(t["recommend"], type="primary", use_container_width=True):
        st.session_state["profile"] = profile
        st.session_state["bundle"] = base_ids
        st.session_state["interests"] = interests
    profile = st.session_state.get("profile", profile)
    base_ids = st.session_state.get("bundle", base_ids)
    if base_ids:
        st.markdown("#### Recommended bundle")
        reasons = {
            "micro": "A low-entry connectivity and billing package for daily UPI/POS work.",
            "prof": "Reliable office connectivity with business email and device protection.",
            "multi": "Multi-site connectivity with failover where the profile meets eligibility.",
            "mfg": "A fit-for-site connection; dedicated links appear only when GSTIN and size rules pass.",
        }
        st.info(f"**{profile['segment']}** · {reasons[profile['segment_code']]}")
        eligible_addons = []
        for _, p in PRODUCTS.iterrows():
            ok, _ = is_eligible(p, profile)
            if ok and p.product_id not in base_ids:
                req = [x for x in str(p.requires_one_of).split("|") if x]
                if req and not any(x in base_ids for x in req):
                    continue
                eligible_addons.append(p.product_id)
        labels = {p.product_id: f"{p.product_name} · from {money(p.price_min_inr_per_month)}/{p.unit}/month" for _, p in PRODUCTS.iterrows()}
        chosen = st.multiselect("Toggle add-ons", eligible_addons, format_func=lambda pid: labels[pid], default=[])
        final_ids = list(dict.fromkeys(base_ids + chosen))
        quote, monthly, setup, term = render_quote(final_ids, profile)
        st.markdown(f"#### {t['quote']}")
        st.dataframe(quote, use_container_width=True, hide_index=True)
        a, b, c = st.columns(3)
        a.metric(t["monthly"], money(monthly))
        b.metric(t["setup"], money(setup))
        c.metric("Minimum bundle term", f"{term} months")
        st.caption("Prices use catalogue starting rates; taxes and site feasibility are confirmed before checkout.")
        st.button("Continue to consent-led KYC", use_container_width=True, on_click=lambda: st.session_state.update({"last_quote": {"monthly": monthly, "setup": setup, "products": final_ids}}))
    else:
        st.warning("No eligible catalogue product matches this profile. Route the lead to a partner for a site check.")


elif page == t["kyc"]:
    st.subheader(t["kyc"])
    st.markdown("This demo uses fictional specimen documents and mock registries. It does not contact government systems.")
    consent = st.checkbox(t["consent"])
    if not consent:
        st.info("Consent is required before this demonstration can show a lookup.")
        st.stop()
    st.caption(t["privacy"])
    samples = {
        "K04 · Saffron Dental Care LLP · active match": {
            "gstin": "27PZSXS1936O1ZH", "udyam": "UDYAM-MH-00-6131836", "name": "Saffron Dental Care LLP", "files": ["K04_gst_certificate.png", "K04_udyam_certificate.png", "K04_address_proof.png", "K04_signatory_id.png"]
        },
        "K01 · Vindhya Tours & Travels · cancelled GSTIN": {
            "gstin": "37IHKXV5167L1ZS", "udyam": "", "name": "Vindhya Tours & Travels", "files": ["K01_gst_certificate.png", "K01_udyam_certificate.png", "K01_address_proof.png", "K01_signatory_id.png"]
        },
        "K05 · sample with missing Udyam document": {
            "gstin": "", "udyam": "", "name": "Sample applicant K05", "files": ["K05_gst_certificate.png", "K05_address_proof.png", "K05_signatory_id.png"]
        },
    }
    case_name = st.selectbox("Specimen scenario", list(samples))
    case = samples[case_name]
    sample_id = case_name.split(" · ", 1)[0].lower()
    uploaded = st.file_uploader("Upload specimen document(s)", type=["png", "jpg", "jpeg", "pdf"], accept_multiple_files=True)
    if uploaded:
        st.caption(f"{len(uploaded)} file(s) received in session memory; no file is written to disk.")
    use_fixture = st.checkbox("Use the bundled synthetic KYC specimen for simulated OCR", value=True)
    simulate_mismatch = st.checkbox("Simulate a legal-name mismatch for review")
    gstin = st.text_input("GSTIN", value=case["gstin"], max_chars=15, key=f"{sample_id}_gstin")
    udyam_no = st.text_input("Udyam number", value=case["udyam"], max_chars=25, key=f"{sample_id}_udyam")
    extracted_name = st.text_input("Simulated OCR · extracted business name", value=case["name"], key=f"{sample_id}_ocr_name")
    if simulate_mismatch:
        extracted_name = st.text_input("Edited OCR name (mismatch test)", value="Different Demo Business")
    if st.button("Run mock lookups", type="primary"):
        gst_match = GST[GST.gstin.astype(str).str.upper() == gstin.strip().upper()] if gstin else GST.iloc[0:0]
        u_match = UDYAM[UDYAM.udyam_number.astype(str).str.upper() == udyam_no.strip().upper()] if udyam_no else UDYAM.iloc[0:0]
        issue = []
        if not uploaded and not use_fixture:
            issue.append("No document uploaded or selected")
        if not gstin:
            issue.append("GSTIN missing")
        elif gst_match.empty:
            issue.append("GSTIN not found in mock registry")
        elif str(gst_match.iloc[0].status).lower() != "active":
            issue.append(f"GSTIN status is {gst_match.iloc[0].status}")
        if not udyam_no:
            issue.append("Udyam document/number missing")
        elif u_match.empty:
            issue.append("Udyam number not found in mock registry")
        if not gst_match.empty and norm(extracted_name) not in norm(str(gst_match.iloc[0].legal_name)) and norm(str(gst_match.iloc[0].legal_name)) not in norm(extracted_name):
            issue.append("Extracted name differs from GST registry")
        if not u_match.empty and norm(extracted_name) not in norm(str(u_match.iloc[0].enterprise_name)) and norm(str(u_match.iloc[0].enterprise_name)) not in norm(extracted_name):
            issue.append("Extracted name differs from Udyam registry")
        if issue:
            st.warning(t["review"])
            for item in issue:
                st.write(f"• {item}")
        else:
            st.success(t["verified"])
        if not gst_match.empty:
            rec = gst_match.iloc[0]
            st.write(f"GSTIN: `{gstin[:2]}******{gstin[-3:]}` · status: **{rec.status}** · {rec.state}")
        if not u_match.empty:
            rec = u_match.iloc[0]
            st.write(f"Udyam: `{udyam_no[:9]}******` · {rec.enterprise_type} enterprise · {rec.city}, {rec.state}")
        if use_fixture:
            present = [f for f in case["files"] if (DOCS / f).exists()]
            missing = [kind for kind, needle in [("GST certificate", "gst_certificate"), ("Udyam certificate", "udyam_certificate"), ("Address proof", "address_proof"), ("Signatory ID", "signatory_id")] if not any(needle in f for f in case["files"])]
            st.caption(f"Simulated OCR reviewed {len(present)} available synthetic files. Missing: {', '.join(missing) if missing else 'none in this fixture'}.")
    st.caption("Retention: this prototype keeps uploads in the active Streamlit session only; it does not persist documents or identifiers.")


elif page == t["tracker"]:
    st.subheader(t["tracker"])
    demo_order = st.selectbox("Demo order", ["UDYAM-2026-0012 · clinic bundle", "UDYAM-2026-0007 · retailer bundle", "UDYAM-2026-0021 · partner-assisted"])
    status = st.select_slider("Set the demonstration status", ["Quote accepted", "KYC review", "Site survey", "Installation booked", "Activated"], value="Site survey")
    steps = ["Quote accepted", "KYC review", "Site survey", "Installation booked", "Activated"]
    st.progress((steps.index(status) + 1) / len(steps))
    st.markdown(f"### {status}")
    st.write(f"**Order:** {demo_order.split(' · ')[0]}  \n**Next update:** visible in this tracker; no support call needed.")
    st.caption("Installation dates are illustrative and depend on site feasibility and product-specific lead times.")
    st.write("**Partner handoff:** if a site survey or document check needs help, route the case to the local partner with the customer's consent.")


else:
    st.subheader(t["insights"])
    activated = LEADS[LEADS.outcome == "Activated"].copy()
    total = len(LEADS)
    rate = len(activated) / total
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Leads", f"{total:,}")
    c2.metric("Activated", f"{len(activated):,}", f"{rate:.1%} of leads")
    c3.metric("Mean days to activate", f"{activated.days_lead_to_activation.mean():.1f}")
    c4.metric("Mean status-chase calls", f"{activated.customer_follow_up_calls.mean():.1f}")
    seg = LEADS.groupby("segment").agg(Leads=("lead_id", "count"), Activated=("outcome", lambda x: (x == "Activated").sum()))
    seg["Activation rate"] = seg.Activated / seg.Leads
    st.markdown("#### Activation by segment")
    st.dataframe(seg.sort_values("Activation rate", ascending=False).style.format({"Activation rate": "{:.1%}"}), use_container_width=True)
    drops = LEADS[LEADS.drop_reason.notna() & (LEADS.drop_reason != "")].drop_reason.value_counts().head(8).rename_axis("Drop reason").reset_index(name="Leads")
    st.markdown("#### Largest recorded drop reasons")
    st.bar_chart(drops.set_index("Drop reason"))
    st.warning("The supplied churn field is blank for all rows. The case brief's ₹15,000 CAC baseline differs from the activated-row CSV mean; reconcile before presenting CAC savings.")
    st.caption("All figures come from fictional challenge data. Segment and channel rates describe this sample and do not prove causation.")

