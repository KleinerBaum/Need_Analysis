import re
import streamlit as st
import plotly.graph_objects as go
from utils.field_map import WizardStep, get_fields_for_step, get_fields_by_group
from utils.utils_jobinfo import display_fields_summary

st.set_page_config("Vacalyser Vacancy Data Wizard", page_icon="📝", layout="wide")
st.title("Vacalyser Vacancy Data Wizard")
st.info("Fill in each section below. Data is saved for all toolkit tools.")

# --- Wizard Main Steps ---
for step in WizardStep:
    with st.expander(
        f"{step.name.replace('_', ' ').title()}", expanded=(step == list(WizardStep)[0])
    ):
        fields = get_fields_for_step(step)
        cols = st.columns(2)
        for idx, field in enumerate(fields):
            k, label, widget = field["key"], field["label"], field["widget"]
            val = st.session_state.get(k, "")
            opts = field.get("opts", None)
            if widget == "text_input":
                st.session_state[k] = cols[idx % 2].text_input(label, value=val, key=k)
            elif widget == "text_area":
                st.session_state[k] = cols[idx % 2].text_area(label, value=val, key=k)
            elif widget == "number_input":
                # Number fields default to 0.0 if empty, float for generality
                st.session_state[k] = cols[idx % 2].number_input(
                    label, value=float(val) if val not in ("", None) else 0.0, key=k
                )
            elif widget == "selectbox":
                st.session_state[k] = cols[idx % 2].selectbox(
                    label, opts, index=opts.index(val) if val in opts else 0, key=k
                )
            elif widget == "multiselect":
                st.session_state[k] = cols[idx % 2].multiselect(
                    label, opts, default=val if isinstance(val, list) else [], key=k
                )
            elif widget == "checkbox":
                st.session_state[k] = cols[idx % 2].checkbox(
                    label, value=bool(val), key=k
                )
        if step == WizardStep.SUMMARY:
            display_fields_summary()
            exp_key = "expected_annual_salary"
            exp_val = st.session_state.get(exp_key, 0.0)
            st.session_state[exp_key] = st.number_input(
                "Erwartetes Jahresgehalt / Expected Annual Salary",
                value=float(exp_val) if exp_val not in ("", None) else 0.0,
                step=1000.0,
                key=exp_key,
            )
            salary_range = str(st.session_state.get("salary_range", ""))
            numbers = [
                float(n.replace(",", "."))
                for n in re.findall(r"\d+[.,]?\d*", salary_range)
            ]
            min_sal = numbers[0] if numbers else 0
            max_sal = numbers[1] if len(numbers) > 1 else min_sal
            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=["Offered Min", "Offered Max", "Expected"],
                    y=[min_sal, max_sal, st.session_state[exp_key]],
                    marker_color=["#1f77b4", "#1f77b4", "#d62728"],
                )
            )
            fig.update_layout(
                title="Salary Expectation vs Offered Range",
                yaxis_title="Annual Salary",
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

# --- Sidebar: Vacancy Data Preview ---
with st.sidebar:
    st.header("📝 Current Vacancy Data (Preview)")
    for step in WizardStep:
        fields_by_group = get_fields_by_group(step)
        # Only show step if any values are present
        step_has_values = any(
            st.session_state.get(f["key"], None)
            for f in [f for g in fields_by_group.values() for f in g]
        )
        if not step_has_values:
            continue
        with st.expander(f"{step.value.replace('_', ' ').title()}"):
            for group, fields in fields_by_group.items():
                group_has_values = any(
                    st.session_state.get(f["key"], None) for f in fields
                )
                if not group_has_values:
                    continue
                st.markdown(f"**{group}**")
                cols = st.columns(2)
                for idx, field in enumerate(fields):
                    val = st.session_state.get(field["key"], None)
                    if val:
                        display_val = (
                            ", ".join(val)
                            if isinstance(val, (list, tuple))
                            else str(val)
                        )
                        cols[idx % 2].markdown(
                            f"<span style='font-size:0.95em'><b>{field['label']}:</b> {display_val}</span>",
                            unsafe_allow_html=True,
                        )
    st.markdown("---")
    st.info("Fill in the wizard first, then use Vacalyser AI tools!")

st.success(
    "When finished, switch to the Vacalyser Tools panel to generate Job Ads, Boolean Strings, Personas and more!"
)

st.caption("Vacalyser · Vacancy Wizard · powered by Streamlit")
