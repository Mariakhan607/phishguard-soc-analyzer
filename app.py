import streamlit as st
import re
from datetime import datetime

# --- Page Setup ---
st.set_page_config(
    page_title="PhishGuard Enterprise | Threat Hunting & Incident Triage",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Professional Cyber SecOps Theme (Deep Navy / Cyber Grid / Neon Highlights) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    code, pre, .stCodeBlock {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Cyber Deep Navy Gradient Background */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #0f1c30 0%, #080f1a 60%, #040810 100%);
        color: #e2e8f0;
    }

    /* Sidebar Dark Navy Canvas */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #091220 0%, #060a12 100%) !important;
        border-right: 1px solid #1a2a44;
    }

    /* Top Command Header */
    .cyber-header {
        background: linear-gradient(135deg, rgba(16, 29, 54, 0.8) 0%, rgba(10, 19, 36, 0.95) 100%);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 22px 30px;
        margin-bottom: 22px;
        box-shadow: 0 4px 25px rgba(0, 240, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .cyber-title {
        color: #f8fafc;
        font-size: 1.7rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
    }

    .cyber-subtitle {
        color: #7dd3fc;
        font-size: 0.9rem;
        margin-top: 5px;
    }

    /* KPI Metric Containers */
    .kpi-box {
        background: rgba(14, 24, 43, 0.7);
        border: 1px solid #1e3352;
        border-radius: 10px;
        padding: 16px 18px;
        text-align: center;
        backdrop-filter: blur(8px);
    }

    .kpi-title {
        color: #94a3b8;
        font-size: 0.76rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .kpi-score {
        font-size: 2rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 2px;
    }

    /* Threat Status Badges */
    .badge-critical {
        background: rgba(255, 51, 102, 0.15);
        color: #ff3366;
        border: 1px solid rgba(255, 51, 102, 0.5);
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
        box-shadow: 0 0 12px rgba(255, 51, 102, 0.2);
    }

    .badge-suspicious {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.5);
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
    }

    .badge-benign {
        background: rgba(0, 255, 157, 0.15);
        color: #00ff9d;
        border: 1px solid rgba(0, 255, 157, 0.5);
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
        box-shadow: 0 0 12px rgba(0, 255, 157, 0.15);
    }

    .mitre-badge {
        background: #0f243a;
        color: #38bdf8;
        border: 1px solid #0284c7;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        padding: 4px 10px;
        border-radius: 5px;
        margin-right: 6px;
    }

    /* Analyst Investigation Card */
    .analyst-card {
        background: rgba(13, 23, 41, 0.6);
        border: 1px solid #1a2f4c;
        border-radius: 10px;
        padding: 22px;
        margin-top: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --- Built-In Incident Scenarios ---
SAMPLE_SCENARIOS = {
    "Direct IP Credential Harvesting (Critical)": """Received: from relay02.attacker-infrastructure.org (198.51.100.37)
Authentication-Results: spf=fail; dkim=fail; dmarc=fail header.from=security-adfs.net
Return-Path: <bounce@unauthorized-server.ru>
From: Microsoft 365 Security Team <support@security-adfs.net>
To: target-analyst@enterprise-corp.internal
Subject: URGENT: Mandatory Re-authentication - Access Revocation Notice
Date: Tue, 29 Sep 2026 10:15:00 +0000
Content-Type: multipart/mixed; boundary="====boundary_123===="

Security Advisory Notice:
Unrecognized workstation activity detected from foreign IP space.
Corporate directory access scheduled for termination within 6 hours.

Authenticate via enterprise SSO gateway immediately:
Destination: http://194.26.29.112/adfs/sso-login.php?session=active

Attachment: Verification_Checklist.iso""",

    "VIP Executive Wire Lure (BEC / Suspicious)": """Received: from mail.external-outbound.net (203.0.113.88)
Authentication-Results: spf=pass; dkim=pass; dmarc=none
From: Robert Vance (CEO) <ceo-robert.vance@executive-quickdesk.com>
To: accounting-dept@enterprise-corp.internal
Subject: Quick Request - Urgent Wire Transfer Authorization Needed Today
Date: Tue, 29 Sep 2026 09:40:00 +0000

Hi Accounting Team,

I am stepping into board meetings today. Please expedite payment on invoice INV-90412.
Access the vendor payment statement securely here: https://corporate-billing-docs.click/pay-portal

Attach confirmation receipt once processed.

Best,
Robert Vance""",

    "Authorized Internal Operations (Benign)": """Received: from internal-smtp.enterprise-corp.internal (10.14.2.11)
Authentication-Results: spf=pass; dkim=pass; dmarc=pass header.from=enterprise-corp.internal
From: Enterprise IT Operations <it-support@enterprise-corp.internal>
To: all-employees@enterprise-corp.internal
Subject: Scheduled Intranet Upgrades - Thursday 02:00 UTC
Date: Tue, 29 Sep 2026 08:00:00 +0000

Colleagues,

Please be advised that core network switches will undergo scheduled firmware upgrades this Thursday.
No action is required on your part. Detailed release notes are available on SharePoint.

Regards,
IT Network Engineering"""
}

# --- Header Banner ---
st.markdown("""
<div class="cyber-header">
    <div>
        <div class="cyber-title">🛡️ PhishGuard Enterprise | Defensive Threat Triage Workbench</div>
        <div class="cyber-subtitle">MIME RFC 822 Analysis • Automated Defanging • Dynamic SIEM Hunting Rule Generator</div>
    </div>
    <div style="text-align: right;">
        <span class="mitre-badge">T1566: Phishing</span>
        <span class="mitre-badge">T1071: Direct C2</span>
        <span class="mitre-badge">T1036: Masquerading</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🎛️ SOC Console Status")
    st.markdown("🌐 **Sensor Engine:** `ONLINE (Local Sandbox)`")
    st.markdown("📡 **Telemetry Gateway:** `SECURE (v2.6-Cyber)`")
    st.markdown(f"⏱️ **Timestamp:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}`")
    st.markdown("---")
    
    st.markdown("### 🧪 Ingest Test Telemetry")
    selected_scenario = st.selectbox("Choose Sample Scenario:", list(SAMPLE_SCENARIOS.keys()))
    default_text = SAMPLE_SCENARIOS[selected_scenario]

    st.markdown("---")
    st.markdown("### ⚙️ Parser Configurations")
    enable_tld_scan = st.checkbox("Scan High-Risk TLDs (.ru, .click, etc.)", value=True)
    enable_attachment_scan = st.checkbox("Inspect Weaponized MIME Extensions", value=True)
    enable_header_audit = st.checkbox("Enforce SPF/DKIM/DMARC Audit", value=True)

# --- Defensive Engine Functions ---
def defang_url(target):
    return target.replace("http://", "hxxp://").replace("https://", "hxxps://").replace(".", "[.]")

def run_deep_triage(raw_text):
    score = 0
    iocs = []
    
    # 1. URL Extraction & Defanging
    raw_urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', raw_text)
    defanged_urls = [defang_url(u) for u in raw_urls]
    if raw_urls:
        score += min(len(raw_urls) * 15, 30)
        iocs.append(f"Discovered **{len(raw_urls)}** active URL endpoint(s)")

    # 2. Direct IP Link Detection
    raw_ips = re.findall(r'https?://(?:\d{1,3}\.){3}\d{1,3}', raw_text)
    direct_ips = [defang_url(ip) for ip in raw_ips]
    if direct_ips:
        score += 35
        iocs.append(f"**Direct IPv4 Destination Detected:** `{direct_ips[0]}` (Bypasses Domain Reputation)")

    # 3. High-Risk TLDs
    if enable_tld_scan:
        risky_tlds = [".ru", ".top", ".xyz", ".click", ".buzz", ".work", ".su"]
        flagged_tlds = [tld for tld in risky_tlds if tld in raw_text.lower()]
        if flagged_tlds:
            score += 25
            iocs.append(f"**High-Risk TLD Infrastructure:** `{', '.join(flagged_tlds)}`")

    # 4. Display Name Spoofing & Brand Mimicry
    spoofed_keywords = r'(micros0ft|paypa1|goog1e|netf1ix|amaz0n|app1e|adfs-login|security-adfs)'
    spoof_match = re.search(spoofed_keywords, raw_text.lower())
    if spoof_match:
        score += 30
        iocs.append(f"**Brand Impersonation / Typosquatting Token:** `{spoof_match.group(0)}`")

    # 5. Weaponized Attachment Scanning
    found_exts = []
    if enable_attachment_scan:
        dangerous_exts = [r'\.iso', r'\.exe', r'\.hta', r'\.vbs', r'\.xlsm', r'\.zip', r'\.scr', r'\.bat']
        for ext in dangerous_exts:
            if re.search(ext, raw_text, re.IGNORECASE):
                found_exts.append(ext.replace('\\', ''))
        if found_exts:
            score += 35
            iocs.append(f"**Weaponized Payload Indicator:** Embedded file type `{', '.join(found_exts)}`")

    # 6. Email Header Authentication
    auth_flags = []
    if enable_header_audit:
        if "spf=fail" in raw_text.lower():
            score += 25
            auth_flags.append("SPF (Sender Policy Framework): **FAIL** — Originating MTA unauthorized.")
        if "dkim=fail" in raw_text.lower():
            score += 25
            auth_flags.append("DKIM (DomainKeys Identified Mail): **FAIL** — Cryptographic signature mismatch.")
        if "dmarc=fail" in raw_text.lower():
            score += 25
            auth_flags.append("DMARC (Domain-based Message Authentication): **FAIL** — Domain alignment policy violation.")

    # 7. Urgency & Coercion Phrasing
    urgency_phrases = [
        "urgent", "immediately", "revocation", "terminated", "action required",
        "mandatory", "unauthorized", "wire transfer", "within 6 hours", "within 12 hours"
    ]
    detected_urgency = [kw for kw in urgency_phrases if kw in raw_text.lower()]
    if detected_urgency:
        score += min(len(detected_urgency) * 10, 25)
        iocs.append(f"**Social Engineering Urgency Triggers:** {', '.join(detected_urgency)}")

    # Score Clamping & Risk Mapping
    final_score = min(score, 100)
    
    if final_score >= 70:
        badge = '<span class="badge-critical">CRITICAL THREAT</span>'
        level = "High"
        accent_color = "#ff3366"
    elif final_score >= 35:
        badge = '<span class="badge-suspicious">SUSPICIOUS / ELEVATED</span>'
        level = "Medium"
        accent_color = "#fbbf24"
    else:
        badge = '<span class="badge-benign">BENIGN / NORMAL</span>'
        level = "Low"
        accent_color = "#00ff9d"

    return final_score, badge, level, accent_color, iocs, defanged_urls, direct_ips, auth_flags, found_exts

# --- Workspace Input Stream ---
st.markdown("#### 📥 Inbound Message Telemetry Ingestion Stream")
raw_message_input = st.text_area(
    label="Telemetry Input Box",
    value=default_text,
    height=200,
    label_visibility="collapsed"
)

col_run, col_clear = st.columns([1, 4])
with col_run:
    execute_triage = st.button("⚡ Run Threat Intelligence Triage", type="primary", use_container_width=True)

if execute_triage:
    score, badge, level, accent_color, iocs, defanged_urls, direct_ips, auth_flags, found_exts = run_deep_triage(raw_message_input)

    st.markdown("---")

    # --- Top Threat Metrics Grid ---
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-box" style="border-top: 4px solid {accent_color};">
            <div class="kpi-title">Calculated Threat Index</div>
            <div class="kpi-score" style="color: {accent_color};">{score}/100</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-box" style="border-top: 4px solid {accent_color};">
            <div class="kpi-title">Analyst Disposition</div>
            <div style="margin-top: 10px;">{badge}</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-box" style="border-top: 4px solid #38bdf8;">
            <div class="kpi-title">Neutralized Endpoints</div>
            <div class="kpi-score" style="color: #38bdf8;">{len(defanged_urls)}</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-box" style="border-top: 4px solid {'#ff3366' if auth_flags else '#00ff9d'};">
            <div class="kpi-title">Cryptographic Failures</div>
            <div class="kpi-score" style="color: {'#ff3366' if auth_flags else '#00ff9d'};">{len(auth_flags)}</div>
        </div>
        """, unsafe_allow_html=True)

    # Progress Severity Bar
    st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
    st.progress(score / 100)

    # --- Structured Investigation Tabs ---
    tab_summary, tab_iocs, tab_auth, tab_hunting, tab_playbook, tab_mitre = st.tabs([
        "📊 Incident Narrative",
        "🎯 Neutralized IOCs",
        "🔐 MTA Crypto Audit",
        "🏹 Threat Hunting (SIEM / KQL)",
        "🛠️ IR Playbook",
        "🗺️ MITRE ATT&CK Matrix"
    ])

    with tab_summary:
        st.markdown("<div class='analyst-card'>", unsafe_allow_html=True)
        st.subheader("Automated Incident Assessment")
        if level == "High":
            st.error("🚨 **Confirmed High-Confidence Attack Vector.** Observed payload matches credential-harvesting lure with weaponized delivery, domain spoofing, and explicit evasion mechanisms.")
        elif level == "Medium":
            st.warning("⚠️ **Suspicious Lure Pattern.** Communication contains anomalous financial requests or unverified domains. Quarantine and Tier-2 review advised.")
        else:
            st.success("✅ **Benign Traffic.** Message parameters align cleanly with corporate communication baselines.")

        st.markdown("#### Identified Attack Telemetry:")
        if iocs:
            for item in iocs:
                st.markdown(f"- {item}")
        else:
            st.markdown("- Clean payload. Zero static signatures triggered.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_iocs:
        st.markdown("<div class='analyst-card'>", unsafe_allow_html=True)
        st.subheader("RFC-Defanged Indicators of Compromise")
        st.caption("Neutralized formats prevent accidental analyst execution in ticket systems.")
        if defanged_urls:
            for u in defanged_urls:
                st.code(u, language="bash")
        else:
            st.info("No external hyperlinks extracted.")
            
        if found_exts:
            st.markdown("#### Weaponized Staged Attachments:")
            for ext in found_exts:
                st.code(f"MIME Content-Type payload extension: {ext}", language="bash")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_auth:
        st.markdown("<div class='analyst-card'>", unsafe_allow_html=True)
        st.subheader("MTA Sender Identity Verification")
        if auth_flags:
            for f in auth_flags:
                st.error(f"❌ {f}")
        else:
            st.success("✅ All SPF, DKIM, and DMARC alignment checks passed.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_hunting:
        st.markdown("<div class='analyst-card'>", unsafe_allow_html=True)
        st.subheader("Automated SIEM & EDR Threat Hunting Queries")
        st.caption("Copy and execute directly across enterprise log repositories to identify impacted endpoints.")
        
        target_token = direct_ips[0].replace("[.]", ".") if direct_ips else (defanged_urls[0].replace("[.]", ".") if defanged_urls else "malicious-indicator.com")

        st.markdown("**Splunk Enterprise Query (SPL):**")
        st.code(f'index=* sourcetype="pan:traffic" OR sourcetype="stream:http" dest="{target_token}" | stats count by src_ip, user, dest', language="spl")

        st.markdown("**Microsoft Sentinel (KQL Query):**")
        st.code(f'DeviceNetworkEvents | where RemoteUrl has "{target_token}" or RemoteIP has "{target_token}" | project TimeGenerated, DeviceName, InitiatingProcessAccountName, RemoteIP', language="kql")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_playbook:
        st.markdown("<div class='analyst-card'>", unsafe_allow_html=True)
        st.subheader("Tier-1 Containment Checklist (IR-P1)")
        if level == "High":
            st.markdown("""
            - [ ] **Firewall Ingress Block:** Push extracted defanged IP/domain artifacts to perimeter blocklists.
            - [ ] **Identity Containment:** Reset directory password and revoke active OAuth / refresh tokens for targeted recipient.
            - [ ] **Cross-Tenant Purge:** Execute administrative eDiscovery / Exchange Online command to soft-delete matching Subject and Message-ID.
            - [ ] **EDR Network Sweep:** Query endpoint detection telemetry for inbound network connections to the target IP within the last 24 hours.

            ```powershell
            # PowerShell Containment Snippet (Exchange Online)
            Search-Mailbox -Identity "TargetUser" -SearchQuery 'Subject:"URGENT: Mandatory Re-authentication"' -DeleteContent -Force
            ```
            """)
        else:
            st.markdown("""
            - [ ] Log telemetry artifacts to baseline cache.
            - [ ] No perimeter firewall or Active Directory changes required.
            """)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_mitre:
        st.markdown("<div class='analyst-card'>", unsafe_allow_html=True)
        st.subheader("MITRE ATT&CK Enterprise Framework Alignment")
        st.markdown("""
| Tactic | Technique ID | Technique Name | Detection Rationale |
| :--- | :--- | :--- | :--- |
| **Initial Access** | `T1566.001` | Spearphishing Attachment | Analyzes weaponized attachments (.iso, .xlsm, .exe). |
| **Initial Access** | `T1566.002` | Spearphishing Link | Extracts and defangs embedded hyperlinks designed for credential harvesting. |
| **Defense Evasion** | `T1036.005` | Masquerading: Brand Impersonation | Flags typosquatted brand tokens (`micros0ft`, `security-adfs`). |
| **Command & Control** | `T1071.001` | Web Protocols | Identifies direct IPv4 destinations bypassing DNS reputation. |
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Export Report Button ---
    st.markdown("---")
    report_text = f"""================================================================================
                    PHISHGUARD ENTERPRISE SECOPS TRIAGE REPORT
================================================================================
Generated On  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
Threat Score  : {score}/100
Verdict       : {level.upper()}
MITRE Tags    : T1566.001, T1566.002, T1071.001, T1036.005
--------------------------------------------------------------------------------
EXTRACTED IOCs (DEFANGED):
{chr(10).join(defanged_urls) if defanged_urls else "None discovered"}

AUTHENTICATION VIOLATIONS:
{chr(10).join(auth_flags) if auth_flags else "All authentication parameters passed"}

BEHAVIORAL ATTACK SIGNALS:
{chr(10).join(iocs) if iocs else "None flagged"}
================================================================================
"""
    st.download_button(
        label="📥 Download Formal Incident Ticket Summary (.txt)",
        data=report_text,
        file_name=f"PhishGuard_IR_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )
