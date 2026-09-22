# 🛡️ PhishGuard Enterprise | SecOps Phishing Triage Console

An automated defensive triage console engineered to accelerate Tier-1 Security Operations Center (SOC) workflows by parsing inbound email telemetry, extracting neutralized Indicators of Compromise (IOCs), validating cryptographic mail authentication, and mapping incidents to standard IR playbooks.

---

## 🚀 Key Defensive Capabilities

- **Automated IOC Defanging:** Automatically converts live payloads into RFC-compliant safe indicators (`hxxp://`, `[.]`) to protect analysts from accidental execution.
- **Cryptographic Header Auditing:** Parses MTA authentication headers for SPF, DKIM, and DMARC alignment failures.
- **Heuristic Threat Index:** Combines brand typosquatting regex patterns with social engineering urgency weights to generate a dynamic 0–100 threat score.
- **Incident Playbook Generation:** Outputs containment steps (firewall perimeter blocks, identity token resets, and enterprise eDiscovery purges).
- **One-Click Incident Export:** Generates standardized `.txt` triage summaries for incident ticketing systems.

---

## 🎯 MITRE ATT&CK® Mapping

| Tactic | Technique ID | Technique Name |
| :--- | :--- | :--- |
| **Initial Access** | `T1566.001` | Spearphishing Attachment |
| **Initial Access** | `T1566.002` | Spearphishing Link |
| **Command & Control** | `T1071.001` | Web Protocols (Direct IP C2) |

---

## 🛠️ Tech Stack & Dependencies

- **Language:** Python 3.10+
- **Framework:** Streamlit
- **Parsing Engine:** Regular Expressions (Regex) & RFC 822/MIME Headers

---

## 💻 Installation & Execution

```bash
# Clone the repository
git clone [https://github.com/](https://github.com/)<your-username>/phishguard-soc-analyzer.git

# Navigate into directory
cd phishguard-soc-analyzer

# Install dependencies
pip install streamlit

# Launch console
streamlit run app.py
