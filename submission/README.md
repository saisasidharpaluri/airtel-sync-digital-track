# Project Udyam Digital

A local Streamlit prototype for the Airtel SYNC 2026 Digital Track. It demonstrates a guided bundle advisor, transparent quote, consent-led synthetic KYC checks, a simulated order tracker, and analysis of the supplied fictional lead data.

## Run locally

From this folder, run:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local address printed by Streamlit. No API key, network service, or database is required. The app reads the student data pack from the sibling `6ae1873397bc1_digital/YTL_TrackA_Udyam_Digital_Data` folder.

## Demo limits

- The advisor uses deterministic product-catalogue rules and does not call an LLM.
- KYC lookups use the mock registries. OCR is simulated from the labelled specimen scenario; it is not production OCR or government verification.
- The lead, registry, and document records are fictional challenge data. No uploaded file or identifier is persisted by the app.
- Prices use the catalogue's minimum monthly rates. Taxes, coverage, and installation availability require confirmation in a real deployment.

## Data insight caveats

The sample records 368 activations among 5,000 leads (7.4%). The churn column is empty. The case brief's blended CAC of ₹15,000 differs from the mean `acquisition_cost_inr` among activated CSV rows; do not claim CAC savings until the baseline is reconciled.

## Contents

- `app.py`: end-to-end demo
- `requirements.txt`: runtime dependencies
- `privacy_note.md` / `privacy_note.pdf`: privacy choices
- `architecture.md` / `architecture.png`: architecture description and diagram
- `demo_script.md`: three-minute walkthrough
- `TeamName_CampusName.pptx` / `.pdf`: seven-slide submission deck (placeholders must be replaced before submission)

