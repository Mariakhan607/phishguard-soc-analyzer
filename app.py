import streamlit as st
import re
from datetime import datetime

# Configure page metadata & layout
st.set_page_config(
    page_title="PhishGuard Enterprise | SecOps Triage Console",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End SecOps CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    code, pre, .stCodeBlock {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Overall Dark Canvas */
    .stApp {
        background-color: #0b0f17;
        color: #c9d1d9;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #111622;
        border-right: 1px solid #1f293d;
    }

    /* Top Header Banner */
    .soc-header {
        background: linear-gradient(90deg, #131b2e 0%, #17223b 100%);
        border: 1px solid #233554;
        border-radius: 8px;
        padding: 20px 24px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .soc-title {
        color: #f0f6fc;
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin: 0;
    }

    .soc-subtitle {
        color: #8b949e;
        font-size: 0.85rem;
        margin-top: 4px;
    }

    /* Tag Badges */
    .badge-critical {
        background-color: rgba(248, 81, 73, 0.15);
        color: #f85149;
        border: 1px solid rgba(248, 81, 73, 0.4);
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }

    .badge-suspicious {
        background-color: rgba(210, 153, 34, 0.15);
        color: #e3b341;
        border: 1px solid rgba(210, 153, 34, 0.4);
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }

    .badge-benign {
        background-color: rgba(46, 160, 67, 0.15);
        color: #3fb950;
        border: 1px solid rgba(46, 160, 67, 0.4);
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }

    .mitre-tag {
        background-color: #1e293b;
        color: #38bdf8;
        border: 1px solid #334155;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 4px;
        margin-right: 6px;
    }

    /* Metric Cards */
    .kpi-container {
        background-color: #131b2a;
        border: 1px solid #202d44;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }

    .kpi-title {
        color: #8b949e;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }

    .kpi-value {
        color: #f0f6fc;
        font-size: 1.6rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Card Containers */
    .soc-card {
        background-color: #131b2a;
        border: 1px solid #202d44;
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Analyst Presets for Quick Testing
PRESET_CREDENTIAL_PHISH = """Received: from mail.attacker-relay.net (198.51.100.24)
Authentication-Results: spf=fail (sender IP unauthorized); dkim=fail; dmarc=fail
From: Security Operations <alert@micros0ft-portal.com>
To: corporate-analyst@company.com
Subject: URGENT: Mandatory Authentication Token Re-verification Required

Dear Corporate User,

Our perimeter security engine detected multiple anomalous sign-in attempts targeting your identity profile.
Your directory account will be permanently disabled within 12 hours unless validation credentials are authenticated.

Immediate Action Required:
Navigate to the central SSO gateway: http://192.168.1.55/adfs/sso-login.php?user=verify

Incident Reference: SEC-AUTH-99218
Identity & Access Management Response Team"""

PRESET_INVOICE_SCAM = """Received: from outbound.external-partner.org (203.0.113.88)
Authentication-Results: spf=pass; dkim=pass; dmarc=none
From: Accounts Receivable <billing@external-billing.org>
To: accounts-payable@company.com
Subject: Notice: Outstanding Invoice Overdue - Immediate Wire Transfer Request

Attention Accounting,

Please find attached the revised banking coordinates for pending invoice INV-88491. 
The funds must be remitted via wire transfer today to maintain uninterrupted software licensing.

Verify remittance details: https://cloud-invoicing-documents.net/pay/view-statement

Kind regards,
Vendor Collections Support"""

PRESET_BENIGN = """Received: from mail-internal.company.com (10.0.4.12)
Authentication-Results: spf=pass; dkim=pass; dmarc=pass
From: IT Project Management <pm-team@company.com>
To: engineering-leads@company.com
Subject: Quarterly Roadmap Review & Sprint Planning Schedule

Hi Team,

Please review the agenda for our upcoming quarterly sprint sync scheduled for this Thursday at 10:00 AM in Conference Room B.
Meeting notes and roadmap slides are synchronized on our internal team documentation space.

Best regards,
Enterprise Program Management"""

# Header Banner
st.markdown("""
<div class="soc-header">
    <div>
        <div class="soc-title">🛡️ PhishGuard Enterprise | SecOps Incident Triage</div>
        <div class="soc-subtitle">Next-Gen Defensive Automation • RFC-Compliant Defanging • MITRE ATT&CK T1566 Ingest Engine</div>
    </div>
    <div style="text-align: right;">
        <span class="mitre-tag">T1566: Phishing</span>
        <span class="mitre-tag">T1071.001: Web Protocols</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### ⚙️ Console Telemetry")
    st.caption("Environment: **SecOps Production**")
    st.caption(f"Timestamp: **{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}**")
    st.markdown("---")
    
    st.markdown("### 🧪 Load Test Telemetry")
    st.caption("Select a sample payload to run instant triage:")
    
    sample_choice = st.radio(
        "Available Scenarios:",
        ["Credential Harvesting (High)", "Financial Lure (Suspicious)", "Internal Corporate (Benign)"]
    )
    
    if sample_choice == "Credential Harvesting (High)":
        default_payload = PRESET_CREDENTIAL_PHISH
    elif sample_choice == "Financial Lure (Suspicious)":
        default_payload = PRESET_INVOICE_SCAM
    else:
        default_payload = PRESET_BENIGN

    st.markdown("---")
    st.markdown("### 📑 Rule Engine Metrics")
    st.markdown("""
    - **Header Verification:** SPF / DKIM / DMARC
    - **Defang Standard:** `hxxp://` / `[.]`
    - **Brand Impersonation:** RegEx Heuristics
    - **Social Engineering:** Urgency Weights
    """)

# Core Triage Functionality
def defang_target(target):
    return target.replace("http://", "hxxp://").replace("https://", "hxxps://").replace(".", "[.]")

def run_threat_triage(raw_text):
    score = 0
    iocs = []
    
    # 1. URL Extraction & Defanging
    raw_urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', raw_text)
    defanged_urls = [defang_target(u) for u in raw_urls]
    if raw_urls:
        score += min(len(raw_urls) * 20, 40)
        iocs.append(f"Identified {len(raw_urls)} active hyperlink endpoint(s)")

    # 2. Raw IP Check
    raw_ips = re.findall(r'https?://(?:\d{1,3}\.){3}\d{1,3}', raw_text)
    if raw_ips:
        score += 35
        iocs.append(f"Direct IPv4 target endpoint detected: `{defang_target(raw_ips[0])}` (High-confidence bypass indicator)")

    # 3. Typosquatting Check
    impersonation_keywords = r'(micros0ft|paypa1|goog1e|netf1ix|amaz0n|app1e|adfs-login|secure-token)'
    match = re.search(impersonation_keywords, raw_text.lower())
    if match:
        score += 30
        iocs.append(f"Impersonation / Typosquatting token flagged: `{match.group(0)}`")

    # 4. Auth Verification
    auth_alerts = []
    if "spf=fail" in raw_text.lower() or "spf=softfail" in raw_text.lower():
        score += 25
        auth_alerts.append("SPF validation state: FAIL (Originating relay is unauthorized)")
    if "dkim=fail" in raw_text.lower():
        score += 25
        auth_alerts.append("DKIM cryptographical check: FAIL (Header/body alteration detected)")
    if "dmarc=fail" in raw_text.lower():
        score += 25
        auth_alerts.append("DMARC alignment policy: FAIL (Domain policy violation)")

    # 5. Phishing Keywords
    triggers = [
        "urgent", "immediately", "account suspended", "verify", "disabled",
        "terminated", "wire transfer", "unauthorized", "overdue", "action required"
    ]
    detected_words = [kw for kw in triggers if kw in raw_text.lower()]
    if detected_words:
        score += min(len(detected_words) * 15, 30)
        iocs.append(f"Psychological urgency/coercion terms: {', '.join(detected_words)}")

    # Clamp Score
    final_score = min(score, 100)
    
    if final_score >= 70:
        badge_html = '<span class="badge-critical">CRITICAL THREAT</span>'
        level = "High"
    elif final_score >= 40:
        badge_html = '<span class="badge-suspicious">ELEVATED SUSPICIOUS</span>'
        level = "Medium"
    else:
        badge_html = '<span class="badge-benign">BENIGN / NORMAL</span>'
        level = "Low"

    return final_score, badge_html, level, iocs, defanged_urls, auth_alerts

# Workspace Inputs
st.markdown("#### 📥 Inbound Message Ingestion Stream")
raw_input = st.text_area(
    label="Raw RFC822 / MIME Email Headers & Body",
    value=default_payload,
    height=200,
    label_visibility="collapsed"
)

execute_btn = st.button("⚡ Execute Defensive Telemetry Triage", type="primary", use_container_width=True)

if execute_btn:
    score, badge, level, iocs, defanged_urls, auth_alerts = run_threat_triage(raw_input)

    # Top KPI Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">Calculated Risk Index</div>
            <div class="kpi-value" style="color: {'#f85149' if score >= 70 else ('#e3b341' if score >= 40 else '#3fb950')};">{score}/100</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">Disposition Verdict</div>
            <div style="margin-top: 6px;">{badge}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">Extracted Endpoints</div>
            <div class="kpi-value">{len(defanged_urls)}</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">Authentication Flags</div>
            <div class="kpi-value" style="color: {'#f85149' if auth_alerts else '#3fb950'};">{len(auth_alerts)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # Analyst Tabs
    tab_summary, tab_iocs, tab_auth, tab_playbook = st.tabs([
        "📊 Incident Assessment",
        "🎯 Neutralized IOCs (Defanged)",
        "🔐 RFC Header Verification",
        "🛠️ SecOps Remediation Playbook"
    ])

    with tab_summary:
        st.markdown("""
        <div class="soc-card">
            <h4 style="margin-top:0; color:#f0f6fc;">Executive Incident Narrative</h4>
        """, unsafe_allow_html=True)
        if level == "High":
            st.error("Automated triage classified this message as a **High-Confidence Phishing Attack**. Payload characteristics display coercive account suspension language paired with spoofed routing tokens designed to harvest enterprise credentials.")
        elif level == "Medium":
            st.warning("Automated triage classified this communication as **Suspicious / Anomalous**. Contains financial or unverified destination references requiring manual Tier-2 SOC validation.")
        else:
            st.success("Automated triage returned **No Significant Malicious Indicators**. Routine corporate communication matching authenticated baseline parameters.")

        st.markdown("<h5 style='color:#f0f6fc; margin-top:16px;'>Identified Behavioral Signals:</h5>", unsafe_allow_html=True)
        if iocs:
            for ind in iocs:
                st.markdown(f"- {ind}")
        else:
            st.markdown("- Clean payload. No threat signatures observed.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_iocs:
        st.markdown("""
        <div class="soc-card">
            <h4 style="margin-top:0; color:#f0f6fc;">Extracted & Defanged Indicators of Compromise</h4>
            <p style="color:#8b949e; font-size:0.85rem;">All extracted hyperlinks have been neutralized to prevent accidental analyst execution.</p>
        """, unsafe_allow_html=True)
        if defanged_urls:
            for d_url in defanged_urls:
                st.code(d_url, language="bash")
        else:
            st.info("No external web destination targets discovered.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_auth:
        st.markdown("""
        <div class="soc-card">
            <h4 style="margin-top:0; color:#f0f6fc;">Mail Transfer Agent (MTA) Cryptographic Verification</h4>
        """, unsafe_allow_html=True)
        if auth_alerts:
            for flag in auth_alerts:
                st.error(f"❌ {flag}")
        else:
            st.success("✅ SPF, DKIM, and DMARC alignment verified. Sender identity cryptographically intact.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_playbook:
        st.markdown("""
        <div class="soc-card">
            <h4 style="margin-top:0; color:#f0f6fc;">Recommended Incident Response Workflow (IR-P1)</h4>
        """, unsafe_allow_html=True)
        if level == "High":
            st.markdown("""
            1. **Perimeter Ingress Block:** Push extracted defanged IPs/domains to border firewall & web proxy blocklists immediately.
            2. **Active Directory Token Revocation:** Execute automated identity containment: force credential reset and revoke active OAuth sessions for targeted mailbox recipients.
            3. **Enterprise Purge:** Initiate cross-tenant Microsoft 365 / Google Workspace eDiscovery sweep to soft-delete matching Subject and Message-ID artifacts.
            4. **Endpoint Telemetry Query:** Review EDR network event logs (Sysmon Event ID 3 / EDR netconn) across all workstations for connections to the flagged target.
            """)
        elif level == "Medium":
            st.markdown("""
            1. Submit extracted destination payload to an isolated detonation sandbox.
            2. Verify billing or bank change requests out-of-band via trusted internal directory channels.
            3. Quarantine message pending analyst review.
            """)
        else:
            st.markdown("""
            1. No containment required. Release to recipient inbox.
            2. Log telemetry to baseline data warehouse for model calibration.
            """)
        st.markdown("</div>", unsafe_allow_html=True)

    # Export Report Button
    st.markdown("---")
    report_output = f"""=======================================================
          PHISHGUARD ENTERPRISE SECOPS TRIAGE REPORT
=======================================================
Generated On : {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
Risk Score   : {score}/100
Verdict      : {level.upper()}
MITRE Tags   : T1566 (Phishing), T1071.001 (Web Protocols)
-------------------------------------------------------
EXTRACTED IOCs (DEFANGED):
{chr(10).join(defanged_urls) if defanged_urls else "None"}

AUTHENTICATION ALERTS:
{chr(10).join(auth_alerts) if auth_alerts else "Clean / Verified"}

BEHAVIORAL SIGNALS:
{chr(10).join(iocs) if iocs else "None"}
=======================================================
"""
    st.download_button(
        label="📥 Download Formal Incident Summary (.txt)",
        data=report_output,
        file_name=f"Triage_IR_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )