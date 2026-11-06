# Project Udyam Digital

A local Streamlit prototype for the Airtel SYNC 2026 Digital Track. It demonstrates a guided bundle advisor, transparent quote, consent-led synthetic KYC checks, an order tracker, and analysis of the supplied fictional lead data.

## Run locally

From this folder, run:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local address printed by Streamlit. No API key, network service, or database is required to run the prototype. The app reads the student data pack from the sibling `6ae1873397bc1_digital/YTL_TrackA_Udyam_Digital_Data` folder.

## Demo and submission

- `demo_video.avi` is a 51-second narrated walkthrough of the working app, within the brief's three-minute limit.
- `CodeRunners_ABVIIITM.pptx` and `CodeRunners_ABVIIITM.pdf` are the editable seven-slide deck and PDF copy.
- `demo_script.md` contains the exact narration and on-screen sequence. Gnani Timbre voiceover is used; no API key is stored here.
- `privacy_note.md` / `privacy_note.pdf` document the demo data and privacy limits.
- `architecture.md` / `architecture.png` show the prototype architecture.

## Demo limits

- The advisor uses deterministic product-catalogue rules and does not call an LLM.
- KYC lookups use mock registries. OCR is simulated from the labelled specimen scenario; it is not production OCR or government verification.
- The lead, registry and document records are fictional challenge data. No uploaded file or identifier is persisted by the app.
- Prices use the catalogue minimum monthly rates. Taxes, coverage and installation availability require confirmation.
- Business outcomes shown in the deck are pilot hypotheses and sensitivity calculations, not observed results or ROI claims.

## Data insight caveats

The sample records 368 activations among 5,000 leads (7.4%). The churn column is empty. The case brief's blended CAC of ₹15,000 differs from the mean `acquisition_cost_inr` among activated CSV rows (about ₹5,385); do not claim CAC savings until the baseline is reconciled.

## Contents

- `app.py` and `frontend.py`: prototype logic and customer-facing interface
- `requirements.txt`: runtime dependencies
- `privacy_note.md` / `privacy_note.pdf`: privacy choices
- `architecture.md` / `architecture.png`: architecture description and diagram
- `competitive_sources.md`: official-source notes for the comparison slide
- `impact_model.md`: transparent pilot sensitivity assumptions
- `demo_script.md` / `demo_video.avi`: recorded demo assets
- `CodeRunners_ABVIIITM.pptx` / `.pdf`: submission deck files
