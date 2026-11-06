# Solution architecture

```mermaid
flowchart LR
  U[Business owner · English or Hindi] --> UI[Streamlit journey]
  UI --> AD[Guided advisor]
  AD --> CAT[Product catalogue CSV]
  UI --> Q[Quote calculator]
  Q --> CAT
  UI --> K[Consent-led KYC demo]
  K --> OCR[Fixture-backed simulated OCR]
  K --> GST[Mock GSTIN registry CSV]
  K --> UDY[Mock Udyam registry CSV]
  UI --> T[Order tracker · demo state]
  UI --> A[Lead funnel and segment insights]
  A --> LEADS[SMB leads CSV]
  K --> REVIEW[Manual review / local partner handoff]
```

All components run locally in one Streamlit process. There is no external AI provider, database, or government API. The architecture diagram is also included as an editable slide in the submission deck.

