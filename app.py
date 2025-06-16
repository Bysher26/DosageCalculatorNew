import streamlit as st
import pandas as pd
from dosage_calculator import DosageCalculator
from translations import get_translation, LANGUAGES

st.set_page_config(
    page_title="Medical Dosage Calculator",
    page_icon="",
    layout="wide"
)

if 'language' not in st.session_state:
    st.session_state.language = 'en'

def main():
    # Language selector and title/subtitle
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("Peds Critical Care Calculator ")
        st.markdown("Calculate medication dosages and airway equipment sizes based on patient weight and size")
    with col2:
        language = st.selectbox(
            "Language",
            options=['en', 'ar'],
            format_func=lambda x: "🇺🇸 EN" if x == 'en' else "🇸🇦 AR",
            index=0 if st.session_state.language == 'en' else 1,
            key="language_selector",
            label_visibility="collapsed"
        )
    if language != st.session_state.language:
        st.session_state.language = language
        st.experimental_rerun()

    # Inputs: weight + unit side-by-side
    col1, col2, col3 = st.columns(3)
    with col1:
        weight_unit = st.selectbox(
            get_translation("weight_unit", st.session_state.language),
            options=['kg', 'lbs'],
            index=0,
            key="weight_unit_selector"
        )
        weight = st.number_input(
            f"{get_translation('weight', st.session_state.language)} ({weight_unit})",
            min_value=0.1,
            max_value=300.0,
            value=70.0,
            step=0.1,
            format="%.1f"
        )
    with col2:
        age_unit = st.selectbox(
            get_translation("age_unit", st.session_state.language),
            options=['years', 'months'],
            index=0,
            key="age_unit_selector"
        )
        if age_unit == 'years':
            age = st.number_input(
                f"{get_translation('age', st.session_state.language)} ({age_unit})",
                min_value=0,
                max_value=120,
                value=30,
                step=1
            )
        else:
            age = st.number_input(
                f"{get_translation('age', st.session_state.language)} ({age_unit})",
                min_value=0,
                max_value=1440,
                value=360,
                step=1
            )
    with col3:
        calculate_button = st.button(get_translation("calculate", st.session_state.language), type="primary")

    # Convert weight & age to base units
    weight_kg = weight if weight_unit == 'kg' else weight * 0.453592
    age_years = age if age_unit == 'years' else age / 12

    # Validation
    if weight_kg <= 0:
        st.error(get_translation("weight_error", st.session_state.language))
        return
    if age < 0:
        st.error(get_translation("age_error", st.session_state.language))
        return

    calculator = DosageCalculator(weight_kg, age_years)

    if calculate_button or weight_kg > 0:
        st.markdown("---")

        # Patient info with number THEN unit
        st.subheader(get_translation("patient_info", st.session_state.language))
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.metric(
                get_translation("weight", st.session_state.language),
                f"{weight:.1f} {weight_unit}"
            )
        with info_col2:
            st.metric(
                get_translation("age", st.session_state.language),
                f"{age} {get_translation(age_unit, st.session_state.language)}"
            )
        st.markdown("---")

        # Display medication categories
        display_medication_category("intubation", calculator.get_intubation_medications())
        display_medication_category("emergencies", calculator.get_emergency_medications())
        display_medication_category("inotropes", calculator.get_inotropes())
        display_medication_category("sedation", calculator.get_sedation_paralysis())
        display_medication_category("antihypertensives", calculator.get_antihypertensives())
        display_medication_category("antiarrhythmics", calculator.get_antiarrhythmics())
        display_medication_category("airway_defib", calculator.get_airway_defib())  # <- restored with no headers
        display_medication_category("others", calculator.get_others())

def display_medication_category(category_key, medications):
    if not medications:
        return

    st.subheader(get_translation(category_key, st.session_state.language))

    # Airway & Defib category: no table headers
    if category_key == "airway_defib":
        for med in medications:
            dosage = med['dosage']
            if med['name'].lower() == "ett size":
                try:
                    val = float(dosage)
                    dosage = f"{round(val * 2) / 2:.1f}"
                except:
                    pass
            # Propofol dosage fix if in this category (just in case)
            if med['name'].lower() == "propofol":
                dosage = "1-3 mg/kg"
            st.write(f"**{med['name']}**: {dosage} ({med['route']})")
        st.markdown("---")
        return

    # For other categories, show table with headers
    df_data = []
    for med in medications:
        dosage = med['dosage']
        if med['name'].lower() == "ett size":
            try:
                val = float(dosage)
                dosage = f"{round(val * 2) / 2:.1f}"
            except:
                pass
        if med['name'].lower() == "propofol":
            dosage = "1-3 mg/kg"
        df_data.append({
            get_translation("medication", st.session_state.language): med['name'],
            get_translation("dosage", st.session_state.language): dosage,
            get_translation("route", st.session_state.language): med['route']
        })

    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown("---")

if __name__ == "__main__":
    main()


