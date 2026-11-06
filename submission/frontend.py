from __future__ import annotations

import html

import pandas as pd
import streamlit as st


COPY = {
    "English": {
        "eyebrow": "AIRTEL BUSINESS · SMALL BUSINESS ONBOARDING", "brand": "Airtel Business", "top": "Simple setup · Transparent pricing · Human help when you need it",
        "pages": ["Get started", "Verify business", "Track order", "Demo insights"], "hero": "Grow your business with the right connection.", "hero_sub": "Find services that fit your business and get set up with confidence.",
        "steps": ["Business profile", "Choose services", "Verify details", "Track setup"], "profile": "Tell us about your business", "profile_sub": "We’ll use this to find a suitable starting bundle.",
        "type": "Business type", "types": ["Kirana / retail / services", "Clinic / CA / coaching", "Restaurant / multi-site retailer", "Small manufacturer"],
        "tiers": ["Metro / Tier 1", "Other city / Tier 2"], "tier": "City category", "employees": "Team size", "sites": "Business locations",
        "fibre": "Fibre is available at my location", "gst": "I have a GSTIN", "language": "Preferred service language", "recommended": "Recommended for your business",
        "reasons": ["A low-entry connectivity and billing package for daily UPI and POS work.", "Office connectivity with business email and device protection.", "Connectivity for multiple locations, with failover when eligible.", "A fit-for-site connection; dedicated links appear only when eligibility rules pass."],
        "addons": "Make it yours", "addons_sub": "Add services when they suit your needs. Prices update as you choose.", "quote": "Your monthly estimate", "monthly": "Monthly total", "setup": "One-time setup", "term": "Minimum term", "continue": "Continue to business verification", "price_note": "Starting catalogue rates. Taxes, coverage and installation are confirmed before checkout.",
        "no_match": "No eligible catalogue bundle matches this profile. A local partner can help check your site.", "quote_missing": "Build a bundle to see your estimate here.",
        "kyc_title": "Verify your business", "kyc_sub": "Your consent is required before any demonstration lookup.", "demo_notice": "DEMO MODE · Fictional documents and mock registries. No government system is contacted.", "consent": "I agree to use these details for this synthetic KYC demonstration.", "consent_needed": "Give consent to continue with the demonstration.", "privacy": "Uploads stay in this browser session and are not saved by this demo.",
        "scenario": "Synthetic example", "scenarios": ["K04 · Active match", "K01 · Cancelled GSTIN", "K05 · Missing Udyam document"], "upload": "Upload business documents", "fixture": "Use bundled synthetic example", "mismatch": "Simulate a legal-name mismatch for review", "gstin": "GSTIN", "udyam": "Udyam number", "ocr": "Simulated OCR · business name", "run": "Check synthetic registries", "matched": "Registry match found", "review": "Needs a person to review", "no_documents": "No document uploaded or selected", "gst_missing": "GSTIN is missing", "gst_unknown": "GSTIN was not found in the mock registry", "udyam_missing": "Udyam document or number is missing", "udyam_unknown": "Udyam number was not found in the mock registry", "name_gst": "Business name differs from GST registry", "name_udyam": "Business name differs from Udyam registry", "upload_count": "file(s) received in session memory; nothing was written to disk.", "none": "none in this example", "missing": "Missing", "ocr_checked": "Simulated OCR checked", "files": "synthetic files",
        "order_title": "Your order, at a glance", "order_sub": "Follow each step from quote to activation.", "order": "Demo order", "status": "Current order status", "statuses": ["Quote accepted", "KYC review", "Site survey", "Installation booked", "Activated"], "next": "Your next update will appear here. No support call needed.", "install": "Installation dates are illustrative and depend on site feasibility and product lead times.", "partner": "If a site survey or document check needs help, a local partner can assist with your consent.",
        "evidence": "Project evidence", "evidence_sub": "A separate view of the fictional challenge data behind this concept.", "leads": "Leads", "activated": "Activated", "rate": "Activation rate", "days": "Mean days to activate", "calls": "Mean status-chase calls", "segments": "Activation by business segment", "drops": "Most recorded drop reasons", "caveat": "Churn is blank in the supplied data. The case brief’s ₹15,000 CAC differs from the activated-row CSV mean; reconcile before claiming CAC savings.", "fictional": "All figures are fictional challenge data and do not prove causation.", "guided": "Guided catalogue advisor · mock checks · no external AI",
    },
    "हिन्दी": {
        "eyebrow": "एयरटेल बिज़नेस · छोटे व्यवसाय के लिए", "brand": "एयरटेल बिज़नेस", "top": "आसान शुरुआत · साफ़ कीमत · ज़रूरत पर मानवीय सहायता",
        "pages": ["शुरू करें", "व्यवसाय सत्यापन", "ऑर्डर देखें", "डेमो आँकड़े"], "hero": "अपने व्यवसाय को सही कनेक्टिविटी से आगे बढ़ाएँ।", "hero_sub": "अपने व्यवसाय के अनुसार सेवाएँ चुनें और भरोसे के साथ शुरुआत करें।",
        "steps": ["व्यवसाय की जानकारी", "सेवाएँ चुनें", "विवरण सत्यापित करें", "सेटअप देखें"], "profile": "अपने व्यवसाय के बारे में बताएँ", "profile_sub": "इससे आपके लिए उपयुक्त शुरुआती बंडल चुनने में मदद मिलेगी।",
        "type": "व्यवसाय का प्रकार", "types": ["किराना / रिटेल / सेवाएँ", "क्लिनिक / CA / कोचिंग", "रेस्टोरेंट / कई दुकानें", "छोटा निर्माता"],
        "tiers": ["मेट्रो / टियर 1", "अन्य शहर / टियर 2"], "tier": "शहर की श्रेणी", "employees": "टीम का आकार", "sites": "व्यवसाय के स्थान",
        "fibre": "मेरे स्थान पर फाइबर उपलब्ध है", "gst": "मेरे पास GSTIN है", "language": "पसंदीदा सेवा भाषा", "recommended": "आपके व्यवसाय के लिए सुझाव",
        "reasons": ["रोज़ाना UPI और POS उपयोग के लिए किफ़ायती कनेक्टिविटी और बिलिंग।", "बिज़नेस ईमेल और डिवाइस सुरक्षा के साथ ऑफिस कनेक्टिविटी।", "एक से अधिक स्थानों के लिए कनेक्टिविटी और पात्र होने पर बैकअप।", "साइट के अनुसार कनेक्शन; पात्रता पूरी होने पर ही समर्पित लिंक दिखेंगे।"],
        "addons": "अपनी ज़रूरत के अनुसार जोड़ें", "addons_sub": "ज़रूरत के अनुसार सेवाएँ चुनें। कुल कीमत साथ-साथ अपडेट होगी।", "quote": "आपका अनुमानित बिल", "monthly": "मासिक कुल", "setup": "एक बार का सेटअप", "term": "न्यूनतम अवधि", "continue": "व्यवसाय सत्यापन पर जाएँ", "price_note": "कैटलॉग की शुरुआती कीमतें। टैक्स, कवरेज और इंस्टॉलेशन की पुष्टि ऑर्डर से पहले होगी।",
        "no_match": "इस जानकारी के लिए उपयुक्त बंडल नहीं मिला। स्थानीय पार्टनर साइट की उपलब्धता जाँचने में मदद कर सकता है।", "quote_missing": "अपना अनुमान देखने के लिए पहले बंडल चुनें।",
        "kyc_title": "अपने व्यवसाय का सत्यापन करें", "kyc_sub": "डेमो जाँच से पहले आपकी सहमति ज़रूरी है।", "demo_notice": "डेमो मोड · काल्पनिक दस्तावेज़ और नकली रजिस्ट्री। सरकारी सिस्टम से संपर्क नहीं होता।", "consent": "मैं इस सिंथेटिक KYC डेमो के लिए इन विवरणों के उपयोग की सहमति देता/देती हूँ।", "consent_needed": "डेमो जारी रखने के लिए सहमति दें।", "privacy": "अपलोड इसी ब्राउज़र सत्र में रहते हैं; डेमो इन्हें सेव नहीं करता।",
        "scenario": "सिंथेटिक उदाहरण", "scenarios": ["K04 · सक्रिय रिकॉर्ड", "K01 · रद्द GSTIN", "K05 · उद्यम दस्तावेज़ नहीं"], "upload": "व्यवसाय के दस्तावेज़ अपलोड करें", "fixture": "सिंथेटिक उदाहरण उपयोग करें", "mismatch": "नाम का अंतर दिखाएँ और समीक्षा के लिए भेजें", "gstin": "GSTIN", "udyam": "उद्यम नंबर", "ocr": "सिम्युलेटेड OCR · व्यवसाय का नाम", "run": "सिंथेटिक रजिस्ट्री जाँचें", "matched": "रजिस्ट्री रिकॉर्ड मिला", "review": "मानवीय समीक्षा आवश्यक", "no_documents": "कोई दस्तावेज़ अपलोड या चयनित नहीं है", "gst_missing": "GSTIN उपलब्ध नहीं है", "gst_unknown": "नकली रजिस्ट्री में GSTIN नहीं मिला", "udyam_missing": "उद्यम दस्तावेज़ या नंबर उपलब्ध नहीं है", "udyam_unknown": "नकली रजिस्ट्री में उद्यम नंबर नहीं मिला", "name_gst": "व्यवसाय का नाम GST रजिस्ट्री से अलग है", "name_udyam": "व्यवसाय का नाम उद्यम रजिस्ट्री से अलग है", "upload_count": "फ़ाइलें सत्र में प्राप्त हुईं; डिस्क पर सेव नहीं हुईं।", "none": "इस उदाहरण में कोई नहीं", "missing": "गायब", "ocr_checked": "सिम्युलेटेड OCR ने जाँचीं", "files": "सिंथेटिक फ़ाइलें",
        "order_title": "आपके ऑर्डर की स्थिति", "order_sub": "कोटेशन से सक्रिय होने तक हर चरण देखें।", "order": "डेमो ऑर्डर", "status": "ऑर्डर की मौजूदा स्थिति", "statuses": ["कोटेशन स्वीकार", "KYC समीक्षा", "साइट सर्वे", "इंस्टॉलेशन तय", "सक्रिय"], "next": "अगला अपडेट यहाँ दिखेगा। सहायता के लिए कॉल की ज़रूरत नहीं।", "install": "इंस्टॉलेशन की तारीखें उदाहरण के लिए हैं और साइट व सेवा पर निर्भर हैं।", "partner": "साइट सर्वे या दस्तावेज़ जाँच में स्थानीय पार्टनर आपकी सहमति से मदद कर सकता है।",
        "evidence": "प्रोजेक्ट के आँकड़े", "evidence_sub": "इस अवधारणा के पीछे मौजूद काल्पनिक चुनौती डेटा।", "leads": "लीड", "activated": "सक्रिय", "rate": "सक्रियता दर", "days": "सक्रिय होने के औसत दिन", "calls": "स्टेटस पूछने की औसत कॉल", "segments": "व्यवसाय श्रेणी के अनुसार सक्रियता", "drops": "दर्ज किए गए मुख्य कारण", "caveat": "दिए गए डेटा में churn खाली है। केस ब्रीफ़ का ₹15,000 CAC और सक्रिय लीड CSV का औसत अलग है; बचत का दावा करने से पहले जाँचें।", "fictional": "सभी आँकड़े काल्पनिक चुनौती डेटा से हैं और परिणाम सिद्ध नहीं करते।", "guided": "कैटलॉग आधारित सलाह · नकली जाँच · बाहरी AI नहीं",
    },
}

PAGES = ["advisor", "kyc", "tracker", "evidence"]
KINDS = {
    "Kirana / retail / services": ("Micro retail & services", "micro"),
    "Clinic / CA / coaching": ("Professional offices", "prof"),
    "Restaurant / multi-site retailer": ("Small multi-site businesses", "multi"),
    "Small manufacturer": ("Small manufacturers", "mfg"),
}


def render_frontend(PRODUCTS, LEADS, GST, UDYAM, DOCS, money, norm, product_row, is_eligible, quantities, suggested_ids, render_quote):
    st.markdown("""
    <style>
    :root{--airtel:#e4002b;--red-dark:#bd0025;--ink:#172033;--muted:#687386;--line:#e7eaf0;--canvas:#f7f8fb}
    .stApp{background:var(--canvas);color:var(--ink)}[data-testid="stHeader"]{background:rgba(247,248,251,.94)}
    .block-container{max-width:1240px;padding:3.4rem 2rem 3rem}section[data-testid="stSidebar"]{display:none}
    h1,h2,h3{color:var(--ink);letter-spacing:-.035em}.brandbar{display:flex;align-items:center;gap:.8rem;padding:.2rem 0 .8rem}
    .brand-logo{display:grid;place-items:center;width:42px;height:42px;border-radius:14px;background:var(--airtel);color:#fff;font-size:.72rem;font-weight:900;box-shadow:0 7px 18px #e4002b28}
    .brand-name{color:var(--ink);font-weight:800}.brand-sub{color:var(--muted);font-size:.73rem;margin-top:.14rem}.trustline{text-align:right;color:var(--muted);font-size:.78rem;padding:.55rem 0}
    .hero{position:relative;overflow:hidden;border:1px solid #f4d8df;border-radius:24px;padding:1.8rem 2rem;background:linear-gradient(110deg,#fff 0%,#fff 57%,#fff1f4 100%);box-shadow:0 16px 38px #1a27410b;margin:.2rem 0 1.1rem}
    .hero:after{content:"";position:absolute;width:225px;height:225px;border:34px solid #e4002b0c;border-radius:50%;right:-65px;top:-120px}
    .eyebrow{font-size:.7rem;font-weight:800;letter-spacing:.12em;color:var(--airtel);margin:0 0 .6rem}.hero-title{color:var(--ink);font-size:clamp(1.7rem,3vw,2.5rem);font-weight:820;line-height:1.1;max-width:770px;margin:0;letter-spacing:-.05em}.hero-copy{color:#586477;font-size:1rem;max-width:710px;margin:.65rem 0 0}.hero-note{margin-top:.8rem;color:#657085;font-size:.76rem;font-weight:650}
    [data-testid="stSegmentedControl"]{background:#fff;border:1px solid var(--line);border-radius:14px;padding:.3rem}[data-testid="stSegmentedControl"] button{border-radius:10px!important;font-weight:650!important;color:#566175!important}[data-testid="stSegmentedControl"] button[aria-pressed="true"]{background:#fff0f3!important;color:var(--red-dark)!important}
    .journey-step{display:flex;align-items:center;gap:.5rem;padding:.5rem .55rem;border-radius:13px;background:#fff;border:1px solid var(--line);color:#778195;font-size:.72rem;font-weight:700}.journey-step.active{border-color:#f1b5c2;background:#fff1f4;color:var(--red-dark)}.step-dot{display:inline-grid;place-items:center;flex:0 0 22px;width:22px;height:22px;border-radius:50%;background:#eef0f4;color:#647085;font-size:.68rem}.journey-step.active .step-dot{background:var(--airtel);color:#fff}
    [data-testid="stVerticalBlockBorderWrapper"]{border-color:var(--line)!important;border-radius:18px!important;background:#fff;box-shadow:0 8px 25px #1a274109}[data-testid="stMetric"]{background:#fff7f8;border:1px solid #f7e3e7;border-radius:14px;padding:.62rem .8rem}[data-testid="stMetricLabel"]{color:#6c7788!important;font-size:.75rem}[data-testid="stMetricValue"]{color:var(--ink)!important;font-size:1.3rem;font-weight:800}
    .stButton>button{border-radius:11px;min-height:2.7rem;font-weight:750;transition:all .15s ease}.stButton>button[kind="primary"]{background:var(--airtel);border:1px solid var(--airtel);color:#fff;box-shadow:0 8px 18px #e4002b26}.stButton>button[kind="primary"]:hover{background:var(--red-dark);border-color:var(--red-dark);transform:translateY(-1px)}
    .stTextInput input,.stNumberInput input{border-radius:10px!important;background:#fff!important;color:var(--ink)!important}.stTextInput input::placeholder{color:#7b8493!important}[data-testid="stSelectbox"] [data-baseweb="select"]>div,[data-testid="stMultiSelect"] [data-baseweb="select"]>div,[role="combobox"]{border-radius:10px!important;background:#fff!important;background-color:#fff!important;color:var(--ink)!important;border-color:#dfe3ea!important}[data-baseweb="select"] input,[data-baseweb="select"] span,[role="combobox"] *{color:var(--ink)!important}[data-baseweb="popover"],[data-baseweb="popover"]>div,[role="listbox"],[role="option"],[data-baseweb="menu"]{background:#fff!important;background-color:#fff!important;color:var(--ink)!important}[role="option"]:hover{background:#fff0f3!important;color:var(--red-dark)!important}[data-baseweb="tag"]{background:#fff0f3!important;color:var(--red-dark)!important}[data-testid="stFileUploaderDropzone"]{border:1.5px dashed #e3a2b1;background:#fff7f8;border-radius:15px}
    .product-tile{border:1px solid var(--line);border-radius:15px;padding:.9rem;background:#fff;min-height:92px}.product-title{font-weight:750;color:var(--ink);font-size:.9rem}.product-price{color:var(--red-dark);font-weight:750;margin-top:.4rem;font-size:.87rem}
    .notice{border-radius:13px;padding:.8rem .9rem;background:#fff3f5;color:#7c1f35;border:1px solid #f3d2da;font-size:.83rem}.notice-neutral{background:#f5f7fa;color:#485468;border-color:#e6eaf0}.result-good{border:1px solid #b9e5ce;background:#f0fbf5;color:#17653c;border-radius:15px;padding:.9rem 1rem}.result-review{border:1px solid #f3d39d;background:#fff9ed;color:#76500c;border-radius:15px;padding:.9rem 1rem}
    .track-card{text-align:center;min-height:78px;border-radius:13px;padding:.65rem .2rem;border:1px solid var(--line);background:#fff;color:#7b8493;font-size:.71rem;font-weight:650}.track-card.done{color:#17653c;border-color:#c3e8d3;background:#f3fcf6}.track-card.current{color:var(--red-dark);border-color:#f0aab8;background:#fff1f4}.footerline{color:#8a93a1;font-size:.71rem;text-align:center;padding:1.6rem 0 .3rem}
    @media(max-width:720px){.block-container{padding:3.2rem .8rem 2rem}.hero{padding:1.25rem;border-radius:18px}.trustline{text-align:left;font-size:.7rem}.stRadio [role="radiogroup"]{width:100%;flex-wrap:wrap}.stRadio [role="radiogroup"] label{padding:.3rem .4rem;font-size:.74rem}.journey-step{justify-content:center;padding:.36rem .2rem;font-size:.62rem}.journey-step .step-dot{flex-basis:19px;width:19px;height:19px}[data-testid="stMetricValue"]{font-size:1rem}}
    </style>
    """, unsafe_allow_html=True)

    lang_col, brand_col, note_col = st.columns([.8, 1.35, 2.5], vertical_alignment="center")
    with lang_col:
        language = st.segmented_control("Language / भाषा", ["English", "हिन्दी"], default="English", key="language_top", label_visibility="collapsed", width="stretch")
    t = COPY[language]
    with brand_col:
        st.markdown(f'<div class="brandbar"><span class="brand-logo">airtel</span><div><div class="brand-name">{t["brand"]}</div><div class="brand-sub">SYNC · Digital Track</div></div></div>', unsafe_allow_html=True)
    with note_col:
        st.markdown(f'<div class="trustline">{t["top"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<section class="hero"><div class="eyebrow">{t["eyebrow"]}</div><h1 class="hero-title">{t["hero"]}</h1><p class="hero-copy">{t["hero_sub"]}</p><div class="hero-note">{t["guided"]}</div></section>', unsafe_allow_html=True)
    page = st.segmented_control("Journey", PAGES, format_func=lambda key: t["pages"][PAGES.index(key)], default="advisor", label_visibility="collapsed", key="journey", width="stretch", wrap=True)
    page = page or "advisor"

    if page != "evidence":
        active = {"advisor": 0, "kyc": 2, "tracker": 3}[page]
        cols = st.columns(4)
        for i, col in enumerate(cols):
            with col:
                state = "active" if i == active else ""
                st.markdown(f'<div class="journey-step {state}"><span class="step-dot">{i + 1}</span><span>{t["steps"][i]}</span></div>', unsafe_allow_html=True)

    if page == "advisor":
        st.subheader(t["profile"])
        st.caption(t["profile_sub"])
        main, summary = st.columns([1.45, .85], gap="large")
        with main:
            with st.container(border=True):
                kind = st.selectbox(t["type"], list(KINDS), format_func=lambda key: t["types"][list(KINDS).index(key)], key="business_kind")
                c1, c2 = st.columns(2)
                with c1:
                    tier = st.selectbox(t["tier"], [1, 2], format_func=lambda n: t["tiers"][n - 1], key="city_tier")
                    employees = st.number_input(t["employees"], 1, 500, 3, key="employees")
                with c2:
                    sites = st.number_input(t["sites"], 1, 100, 1, key="sites")
                    fibre = st.toggle(t["fibre"], True, key="fiber")
                    gst = st.toggle(t["gst"], True, key="gst")
                st.selectbox(t["language"], ["Hindi", "English", "Marathi", "Telugu", "Tamil", "Kannada", "Gujarati", "Bengali", "Punjabi", "Malayalam"], key="preferred_language")
            segment, code = KINDS[kind]
            profile = {"segment": segment, "segment_code": code, "tier": tier, "employees": int(employees), "sites": int(sites), "fiber": fibre, "gst": gst}
            base_ids = suggested_ids(profile)
            if not base_ids:
                st.warning(t["no_match"])
                final_ids, quote, monthly, setup, term = [], pd.DataFrame(), 0, 0, 0
            else:
                st.markdown(f"#### {t['recommended']}")
                st.caption(t["reasons"][list(KINDS).index(kind)])
                for start in range(0, len(base_ids), 2):
                    cards = st.columns(2)
                    for pid, col in zip(base_ids[start:start + 2], cards):
                        p = product_row(pid)
                        qty = quantities(profile).get(pid, int(profile["sites"]) if p.unit == "per site" else 1)
                        with col:
                            st.markdown(f'<div class="product-tile"><div class="product-title">{html.escape(str(p.product_name))}</div><div class="product-price">{money(float(p.price_min_inr_per_month) * qty)} / month</div><div class="brand-sub">{int(p.min_contract_months)} month minimum</div></div>', unsafe_allow_html=True)
                eligible = []
                for _, product in PRODUCTS.iterrows():
                    ok, _ = is_eligible(product, profile)
                    if ok and product.product_id not in base_ids:
                        req = [x for x in str(product.requires_one_of).split("|") if x]
                        if not req or any(x in base_ids for x in req): eligible.append(product.product_id)
                labels = {p.product_id: f"{p.product_name} · {money(p.price_min_inr_per_month)}/{p.unit}/month" for _, p in PRODUCTS.iterrows()}
                st.markdown(f"#### {t['addons']}")
                st.caption(t["addons_sub"])
                chosen = st.multiselect(t["addons"], eligible, format_func=lambda pid: labels[pid], key="chosen_addons", label_visibility="collapsed")
                final_ids = list(dict.fromkeys(base_ids + chosen))
                quote, monthly, setup, term = render_quote(final_ids, profile)
                st.session_state["last_quote"] = {"monthly": monthly, "setup": setup, "products": final_ids, "term": term}
        with summary:
            with st.container(border=True):
                st.markdown(f"#### {t['quote']}")
                if final_ids:
                    for row in quote.itertuples(index=False):
                        st.markdown(f"**{row.Product}**  \n{int(row.Qty)} × {money(row.Monthly / row.Qty)} · {row.Term}")
                        st.markdown("---")
                    st.metric(t["monthly"], money(monthly))
                    st.metric(t["setup"], money(setup))
                    st.caption(f"{t['term']}: {term} months")
                    st.button(t["continue"], type="primary", use_container_width=True, key="go_to_kyc", on_click=lambda: st.session_state.update({"journey": "kyc"}))
                    st.caption(t["price_note"])
                else:
                    st.caption(t["quote_missing"])
            st.caption(t["privacy"])

    elif page == "kyc":
        st.subheader(t["kyc_title"])
        st.caption(t["kyc_sub"])
        st.markdown(f'<div class="notice">{t["demo_notice"]}</div>', unsafe_allow_html=True)
        with st.container(border=True):
            consent = st.checkbox(t["consent"], key="kyc_consent")
            if not consent:
                st.info(t["consent_needed"])
                st.stop()
            st.caption(t["privacy"])
            samples = {
                "K04": {"gstin": "27PZSXS1936O1ZH", "udyam": "UDYAM-MH-00-6131836", "name": "Saffron Dental Care LLP", "files": ["K04_gst_certificate.png", "K04_udyam_certificate.png", "K04_address_proof.png", "K04_signatory_id.png"]},
                "K01": {"gstin": "37IHKXV5167L1ZS", "udyam": "", "name": "Vindhya Tours & Travels", "files": ["K01_gst_certificate.png", "K01_udyam_certificate.png", "K01_address_proof.png", "K01_signatory_id.png"]},
                "K05": {"gstin": "", "udyam": "", "name": "Sample applicant K05", "files": ["K05_gst_certificate.png", "K05_address_proof.png", "K05_signatory_id.png"]},
            }
            keys = list(samples)
            scenario = st.selectbox(t["scenario"], keys, format_func=lambda key: t["scenarios"][keys.index(key)], key="kyc_scenario")
            case = samples[scenario]
            left, right = st.columns(2, gap="large")
            with left:
                uploaded = st.file_uploader(t["upload"], type=["png", "jpg", "jpeg", "pdf"], accept_multiple_files=True, key="kyc_upload")
                fixture = st.checkbox(t["fixture"], value=True, key="use_kyc_fixture")
                if uploaded: st.caption(f"{len(uploaded)} {t['upload_count']}")
            with right:
                gstin = st.text_input(t["gstin"], value=case["gstin"], max_chars=15, key=f"{scenario.lower()}_gstin")
                udyam = st.text_input(t["udyam"], value=case["udyam"], max_chars=25, key=f"{scenario.lower()}_udyam")
                name = st.text_input(t["ocr"], value=case["name"], key=f"{scenario.lower()}_ocr_name")
            mismatch = st.checkbox(t["mismatch"], key="simulate_name_mismatch")
            if mismatch: name = st.text_input("Edited OCR name / संशोधित नाम", value="Different Demo Business", key="mismatched_ocr_name")
            if st.button(t["run"], type="primary", key="run_mock_kyc"):
                gst_match = GST[GST.gstin.astype(str).str.upper() == gstin.strip().upper()] if gstin else GST.iloc[0:0]
                u_match = UDYAM[UDYAM.udyam_number.astype(str).str.upper() == udyam.strip().upper()] if udyam else UDYAM.iloc[0:0]
                issues = []
                if not uploaded and not fixture: issues.append(t["no_documents"])
                if not gstin: issues.append(t["gst_missing"])
                elif gst_match.empty: issues.append(t["gst_unknown"])
                elif str(gst_match.iloc[0].status).lower() != "active": issues.append(f"GSTIN status: {gst_match.iloc[0].status}")
                if not udyam: issues.append(t["udyam_missing"])
                elif u_match.empty: issues.append(t["udyam_unknown"])
                if not gst_match.empty and norm(name) not in norm(str(gst_match.iloc[0].legal_name)) and norm(str(gst_match.iloc[0].legal_name)) not in norm(name): issues.append(t["name_gst"])
                if not u_match.empty and norm(name) not in norm(str(u_match.iloc[0].enterprise_name)) and norm(str(u_match.iloc[0].enterprise_name)) not in norm(name): issues.append(t["name_udyam"])
                missing = [label for label, needle in [("GST certificate", "gst_certificate"), ("Udyam certificate", "udyam_certificate"), ("Address proof", "address_proof"), ("Signatory ID", "signatory_id")] if not any(needle in file for file in case["files"])]
                st.session_state["kyc_result"] = {"scenario": scenario, "issues": issues, "gst_match": gst_match, "u_match": u_match, "gstin": gstin, "udyam": udyam, "count": len([f for f in case["files"] if (DOCS / f).exists()]) if fixture else 0, "missing": missing, "fixture": fixture}
            result = st.session_state.get("kyc_result")
            if result and result["scenario"] == scenario:
                if result["issues"]:
                    st.markdown(f'<div class="result-review"><strong>⚠ {t["review"]}</strong></div>', unsafe_allow_html=True)
                    for issue in result["issues"]: st.write(f"• {issue}")
                else: st.markdown(f'<div class="result-good"><strong>✓ {t["matched"]}</strong></div>', unsafe_allow_html=True)
                if not result["gst_match"].empty:
                    row = result["gst_match"].iloc[0]
                    st.write(f"GSTIN: `{result['gstin'][:2]}******{result['gstin'][-3:]}` · **{row.status}** · {row.state}")
                if not result["u_match"].empty:
                    row = result["u_match"].iloc[0]
                    st.write(f"Udyam: `{result['udyam'][:9]}******` · {row.enterprise_type} · {row.city}, {row.state}")
                if result["fixture"]:
                    missing_text = ", ".join(result["missing"]) if result["missing"] else t["none"]
                    st.caption(f"{t['ocr_checked']} {result['count']} {t['files']}. {t['missing']}: {missing_text}.")

    elif page == "tracker":
        st.subheader(t["order_title"])
        st.caption(t["order_sub"])
        orders = ["UDYAM-2026-0012 · clinic bundle", "UDYAM-2026-0007 · retailer bundle", "UDYAM-2026-0021 · partner-assisted"]
        st.selectbox(t["order"], orders, key="demo_order")
        status = st.select_slider(t["status"], list(range(5)), value=2, format_func=lambda i: t["statuses"][i], key="tracker_status")
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                state = "done" if i < status else "current" if i == status else ""
                icon = "✓" if i < status else "●" if i == status else "○"
                st.markdown(f'<div class="track-card {state}"><div style="font-size:1.2rem">{icon}</div>{t["statuses"][i]}</div>', unsafe_allow_html=True)
        st.progress((status + 1) / 5)
        with st.container(border=True):
            st.markdown(f"**{t['status']}**")
            st.markdown(f"### {t['statuses'][status]}")
            st.write(t["next"])
            st.caption(t["install"])
            st.info(t["partner"])

    else:
        st.subheader(t["evidence"])
        st.caption(t["evidence_sub"])
        activated = LEADS[LEADS.outcome == "Activated"].copy()
        total = len(LEADS)
        rate = len(activated) / total if total else 0
        a, b, c, d = st.columns(4)
        a.metric(t["leads"], f"{total:,}")
        b.metric(t["activated"], f"{len(activated):,}", f"{rate:.1%} {t['rate'].lower()}")
        c.metric(t["days"], f"{activated.days_lead_to_activation.mean():.1f}")
        d.metric(t["calls"], f"{activated.customer_follow_up_calls.mean():.1f}")
        segment = LEADS.groupby("segment").agg(Leads=("lead_id", "count"), Activated=("outcome", lambda values: (values == "Activated").sum()))
        segment[t["rate"]] = segment.Activated / segment.Leads
        left, right = st.columns([1.1, .9], gap="large")
        with left:
            with st.container(border=True):
                st.markdown(f"#### {t['segments']}")
                st.dataframe(segment.sort_values(t["rate"], ascending=False).style.format({t["rate"]: "{:.1%}"}), use_container_width=True)
        drops = LEADS[LEADS.drop_reason.notna() & (LEADS.drop_reason != "")].drop_reason.value_counts().head(8).rename_axis("Drop reason").reset_index(name="Leads")
        with right:
            with st.container(border=True):
                st.markdown(f"#### {t['drops']}")
                st.bar_chart(drops.set_index("Drop reason"))
        st.warning(t["caveat"])
        st.caption(t["fictional"])

    st.markdown('<div class="footerline">Airtel SYNC · Digital Track · Guided catalogue demo</div>', unsafe_allow_html=True)
