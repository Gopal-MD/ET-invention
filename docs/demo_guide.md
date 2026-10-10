# 3-5 Minute Demo

1. Open the dashboard and point out the linked counts for obligations, controls, evidence coverage, and open gaps.
2. Open **Regulatory Library** and upload a small `.txt` source document. Explain that it is stored as an unverified source until reviewed.
3. Open **Assessments**, run the quarterly reporting assessment, and show the stages from retrieval through risk and remediation.
4. Highlight the missing certification page. Explain that document existence alone is not treated as compliance evidence.
5. Show the deterministic score and thresholds. The formula is `Impact x Likelihood x Regulatory Criticality`; the prototype value is not an official regulatory threshold.
6. Open **Remediation Center**, approve the proposal, then open **Audit Trail** to show the approval event.
7. Open **Regulatory Changes** and show the v1/v2 source-backed change comparison.

Without `GROQ_API_KEY`, this demo uses deterministic rules and synthetic records. The UI/API identify that mode explicitly. With a server-side key, `/api/v1/assistant` can provide bounded explanations, but human review remains required.