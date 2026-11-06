# Privacy and security note — Project Udyam Digital

This prototype uses only the fictional challenge dataset and specimen documents. It does not contact GST, Udyam, DigiLocker, e-sign, Airtel, or any other external service.

Before the KYC demonstration, the user sees a purpose-specific consent checkbox. The demo uses the details only to illustrate mock document and registry checks. It masks identifiers in its results, keeps uploaded files in the active browser session, and writes no document or identifier to disk or a database. Closing or restarting the app clears the demonstration session.

Mock GSTIN and Udyam lookups compare against the supplied synthetic registries. They do not establish the legal identity or status of a real business. Sample OCR values are fixture-backed simulations, not OCR output. Any missing, inactive, or mismatched value is routed to manual review; the prototype never claims automatic approval.

A production service would require a documented retention period, access controls, encryption in transit and at rest, audit logging with masked identifiers, purpose limitation, a deletion workflow, and validated integrations with authorised registries. Production processing should follow applicable Indian privacy requirements, including the DPDP Act, 2023, and be reviewed by the organisation's privacy and security teams.

