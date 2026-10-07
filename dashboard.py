import streamlit as st
import requests
import re


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Campus360 AI",
    page_icon="🏢",
    layout="wide",
)


# ============================================================
# CONFIG
# ============================================================

API_URL = "http://127.0.0.1:8000/api/ai/dashboard"


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .title {
        font-size: 40px;
        font-weight: 750;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 17px;
        opacity: 0.70;
        margin-bottom: 25px;
    }

    .priority-high {
        font-size: 30px;
        font-weight: 750;
        color: #ff4b4b;
    }

    .priority-medium {
        font-size: 30px;
        font-weight: 750;
        color: #ffa726;
    }

    .priority-low {
        font-size: 30px;
        font-weight: 750;
        color: #21c354;
    }

    .decision-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 15px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# API
# ============================================================

@st.cache_data(ttl=30)
def get_pipeline():

    try:

        response = requests.get(
            API_URL,
            timeout=180
        )

        response.raise_for_status()

        return response.json(), None

    except Exception as exc:

        return None, str(exc)


# ============================================================
# PARSING HELPERS
# ============================================================

def extract_single(
    text,
    label,
    default="UNKNOWN"
):

    pattern = (
        rf"{re.escape(label)}:\s*(.+)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:

        return match.group(1).strip()

    return default


def extract_multiline(
    text,
    label,
    next_label,
    default="Not available."
):

    pattern = (
        rf"{re.escape(label)}:\s*(.*?)"
        rf"\n\s*{re.escape(next_label)}:"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:

        return " ".join(
            match.group(1).strip().split()
        )

    return default


def extract_number(
    text,
    label,
    default=0.0
):

    value = extract_single(
        text,
        label,
        ""
    )

    match = re.search(
        r"-?\d+(?:\.\d+)?",
        value
    )

    if match:

        try:
            return float(
                match.group()
            )

        except Exception:
            pass

    return default


def parse_output(output):

    data = {}

    # --------------------------------------------------------
    # Basic facility information
    # --------------------------------------------------------

    data["facility"] = extract_single(
        output,
        "FACILITY"
    )

    data["building"] = extract_single(
        output,
        "BUILDING"
    )

    data["priority"] = extract_single(
        output,
        "PRIORITY"
    )

    data["confidence"] = extract_single(
        output,
        "CONFIDENCE"
    )

    # --------------------------------------------------------
    # Energy
    # --------------------------------------------------------

    energy = extract_single(
        output,
        "CURRENT ENERGY"
    )

    data["energy"] = energy

    # --------------------------------------------------------
    # Explanation
    # --------------------------------------------------------

    data["explanation"] = extract_multiline(
        output,
        "EXPLANATION",
        "RECOMMENDATION"
    )

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    data["recommendation"] = extract_multiline(
        output,
        "RECOMMENDATION",
        "FORECAST"
    )

    # --------------------------------------------------------
    # Forecast
    # --------------------------------------------------------

    data["forecast"] = extract_single(
        output,
        "FORECAST"
    )

    # --------------------------------------------------------
    # Evidence
    # --------------------------------------------------------

    evidence = []

    evidence_section = re.search(
        r"ADVANCED SEMANTIC RAG EVIDENCE:\s*"
        r"(.*?)"
        r"\n\s*Evidence count:",
        output,
        re.IGNORECASE | re.DOTALL
    )

    if evidence_section:

        block = evidence_section.group(1)

        matches = re.findall(
            r"^\s*(.+?)\s*->\s*([0-9.]+)",
            block,
            re.MULTILINE
        )

        for source, score in matches:

            evidence.append(
                {
                    "source": source.strip(),
                    "score": float(score)
                }
            )

    data["evidence"] = evidence

    # --------------------------------------------------------
    # Evidence count
    # --------------------------------------------------------

    data["evidence_count"] = int(
        extract_number(
            output,
            "Evidence count",
            len(evidence)
        )
    )

    # --------------------------------------------------------
    # What-if
    # --------------------------------------------------------

    data["projected"] = extract_number(
        output,
        "Projected consumption"
    )

    data["saved"] = extract_number(
        output,
        "Energy saved"
    )

    data["cost_saving"] = extract_number(
        output,
        "Estimated cost saving"
    )

    data["co2"] = extract_number(
        output,
        "Estimated CO2 reduction"
    )

    # --------------------------------------------------------
    # System modules
    # --------------------------------------------------------

    modules = [
        "Backend telemetry",
        "Anomaly detection",
        "KPI extraction",
        "Forecast layer",
        "Advanced semantic RAG",
        "Decision reasoning",
        "What-if simulation"
    ]

    data["modules"] = modules

    return data


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">🏢 Campus360 AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    "AI-Powered Facility Intelligence & Decision Support"
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🏢 Campus360")

    st.write(
        "EcoFacility Smart Campus"
    )

    st.divider()

    st.subheader(
        "AI Intelligence Modules"
    )

    st.success("✓ Backend Telemetry")
    st.success("✓ Anomaly Detection")
    st.success("✓ KPI Extraction")
    st.success("✓ Forecasting")
    st.success("✓ Semantic RAG")
    st.success("✓ Decision Reasoning")
    st.success("✓ What-If Simulation")

    st.divider()

    if st.button(
        "🔄 Refresh AI Analysis",
        use_container_width=True
    ):

        st.cache_data.clear()

        st.rerun()


# ============================================================
# LOAD DATA
# ============================================================

response_data, error = get_pipeline()


if error:

    st.error(
        "Cannot connect to Campus360 FastAPI."
    )

    st.code(
        error
    )

    st.info(
        "Keep the backend running with:"
    )

    st.code(
        "python -m uvicorn backend.main:app --reload"
    )

    st.stop()


# ============================================================
# VALIDATE RESPONSE
# ============================================================

if not response_data:

    st.error(
        "Empty response received from AI backend."
    )

    st.stop()


if response_data.get(
    "status"
) != "success":

    st.error(
        "AI pipeline returned an error."
    )

    st.json(
        response_data
    )

    st.stop()


output = response_data.get(
    "ai_output",
    ""
)


if not output:

    st.error(
        "The AI backend did not return pipeline output."
    )

    st.stop()


# ============================================================
# PARSE
# ============================================================

data = parse_output(
    output
)


# ============================================================
# FACILITY INFORMATION
# ============================================================

c1, c2, c3 = st.columns(
    [2, 2, 1]
)

with c1:

    st.caption(
        "FACILITY"
    )

    st.subheader(
        data["facility"]
    )

with c2:

    st.caption(
        "BUILDING"
    )

    st.subheader(
        data["building"]
    )

with c3:

    st.caption(
        "AI STATUS"
    )

    st.success(
        "ONLINE"
    )


st.divider()


# ============================================================
# AI DECISION
# ============================================================

st.markdown(
    '<div class="section-title">🎯 AI Decision</div>',
    unsafe_allow_html=True
)

d1, d2 = st.columns(
    2
)

priority = data["priority"].upper()


with d1:

    if priority == "HIGH":

        css_class = "priority-high"

    elif priority == "MEDIUM":

        css_class = "priority-medium"

    else:

        css_class = "priority-low"

    st.markdown(
        f"""
        <div class="{css_class}">
        {priority}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Operational Priority"
    )


with d2:

    st.metric(
        "AI Confidence",
        data["confidence"]
    )


# ============================================================
# CURRENT ENERGY
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">⚡ Facility Energy</div>',
    unsafe_allow_html=True
)

st.metric(
    "Current Energy Consumption",
    data["energy"]
)


# ============================================================
# FORECAST
# ============================================================

st.divider()

f1, f2 = st.columns(
    2
)

with f1:

    st.subheader(
        "📈 Short-Term Forecast"
    )

    forecast = data["forecast"].upper()

    if forecast == "INCREASING":

        st.warning(
            "↑ Energy demand is increasing"
        )

    elif forecast == "DECREASING":

        st.success(
            "↓ Energy demand is decreasing"
        )

    else:

        st.info(
            forecast
        )


with f2:

    st.subheader(
        "🔎 AI Monitoring"
    )

    st.info(
        "The intelligence engine continuously "
        "combines telemetry, anomaly detection, "
        "forecasting and operational knowledge."
    )


# ============================================================
# EXPLANATION
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🧠 AI Explanation</div>',
    unsafe_allow_html=True
)

st.info(
    data["explanation"]
)


# ============================================================
# RECOMMENDATION
# ============================================================

st.subheader(
    "💡 Recommended Action"
)

st.success(
    data["recommendation"]
)


# ============================================================
# RAG EVIDENCE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📚 Advanced Semantic RAG Evidence</div>',
    unsafe_allow_html=True
)

if data["evidence"]:

    for item in data["evidence"]:

        source = item["source"]

        score = item["score"]

        st.write(
            f"**{source}**"
        )

        st.progress(
            min(
                max(score, 0.0),
                1.0
            )
        )

        st.caption(
            f"Semantic relevance: {score:.4f}"
        )

else:

    st.info(
        "No semantic evidence returned."
    )


st.caption(
    f"Evidence sources retrieved: "
    f"{data['evidence_count']}"
)


# ============================================================
# WHAT-IF
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🔮 What-If Impact Simulation</div>',
    unsafe_allow_html=True
)

w1, w2, w3, w4 = st.columns(
    4
)

with w1:

    st.metric(
        "Projected Consumption",
        f"{data['projected']:.2f}"
    )

with w2:

    st.metric(
        "Energy Saved",
        f"{data['saved']:.2f}"
    )

with w3:

    st.metric(
        "Cost Saving",
        f"₹{data['cost_saving']:,.2f}/day"
    )

with w4:

    st.metric(
        "CO₂ Reduction",
        f"{data['co2']:,.2f} kg"
    )


# ============================================================
# SYSTEM STATUS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">⚙️ AI System Status</div>',
    unsafe_allow_html=True
)

cols = st.columns(
    4
)

for index, module in enumerate(
    data["modules"]
):

    with cols[index % 4]:

        st.success(
            f"✓ {module}"
        )


# ============================================================
# RAW AI OUTPUT
# ============================================================

with st.expander(
    "🔧 View Raw AI Pipeline Output"
):

    st.code(
        output,
        language="text"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Campus360 AI • Explainable Facility Intelligence • "
    "Anomaly Detection • Forecasting • Semantic RAG • "
    "Decision Intelligence • What-If Simulation"
)