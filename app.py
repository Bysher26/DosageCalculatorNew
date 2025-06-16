import streamlit as st
import pandas as pd
from dosage_calculator import DosageCalculator
from translations import get_translation, LANGUAGES

# Page configuration
st.set_page_config(
    page_title="Medical Dosage Calculator",
    page_icon="💊",
    layout="wide"
)

# Initialize session state
if 'language' not in st.session_state:
    st.session_state.language = 'en'

def main():
    # Language selector in top-right corner
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Updated title and subtitle here:
        st.title("Peds Critical Care Calculator 💉")
        st.markdown("Calculate medication dosages and airway equipment sizes based on patient weight and size")
    
    with col2:
        st.write("")  # Add some space
        language = st.selectbox(
            "Language",
            options=['en', 'ar'],
            format_func=lambda x: "🇺🇸 EN" if x == 'en' else "🇸🇦 AR",
            index=0 if st.session_state.language == 'en' else 1,
            key="language_selector",
            label_visibility="collapsed",
            disabled=False
        )
    
    if language != st.session_state.language:
        st.session_state.language = language
        st.rerun()
    
    # Input section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Weight input and unit side-by-side
        weight_col1, weight_col2 = st.columns([1, 2])
        with weight_col1:
            weight_unit = st.selectbox(
                get_translation("weight_unit", st.session_state.language),
                options=['kg', 'lbs'],
                index=0,
                key="weight_unit_selector"
            )
        with weight_col2:
            weight = st.number_input(
                get_translation("weight", st.session_state.language),
                min_value=0.1,
                max_value=300.0,
                value=70.0,
                step=0.1,
                format="%.1f"
            )
    
    with col2:
        # Age input and unit side-by-side
        age_col1, age_col2 = st.columns([1, 2])
        with age_col1:
            age_unit = st.selectbox(
                get_translation("age_unit", st.session_state.language),
                options=['years', 'months'],
                index=0,
                key="age_unit_selector"
            )
        with age_col2:
            if age_unit == 'years':
                age = st.number_input(
                    get_translation("age", st.session_state.language),
                    min_value=0,
                    max_value=120,
                    value=30,
                    step=1
                )
            else:  # months
                age = st.number_input(
                    get_translation("age", st.session_state.language),
                    min_value=0,
                    max_value=1440,  # 120 years * 12 months
                    value=360,  # 30 years * 12 months
                    step=1
                )
    
    with col3:
        st.write("")  # Spacer
        calculate_button = st.button(
            get_translation("calculate", st.session_state.language),
            type="primary"
        )
    
    # Convert weight to kg if needed
    weight_kg = weight if weight_unit == 'kg' else weight * 0.453592
    
    # Convert age to years if needed
    age_years = age if age_unit == 'years' else age / 12
    
    # Validation
    if weight_kg <= 0:
        st.error(get_translation("weight_error", st.session_state.language))
        return
    
    if age < 0:
        st.error(get_translation("age_error", st.session_state.language))
        return
    
    # Calculate dosages
    calculator = DosageCalculator(weight_kg, age_years)
    
    if calculate_button or weight_kg > 0:
        st.markdown("---")
        
        # Display patient info with unit after value
        st.subheader(get_translation("patient_info", st.session_state.language))
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.metric(
                get_translation("weight", st.session_state.language),
                f"{weight:.1f} {weight_unit}"
            )
        with info_col2:
            age_display = f"{age} " + get_translation(age_unit, st.session_state.language)
            st.metric(
                get_translation("age", st.session_state.language),
                age_display
            )
        
        st.markdown("---")
        
        # Display medication categories without "airway & defib" subtitle
        # Skip subtitle for "airway_defib"
        display_medication_category("intubation", calculator.get_intubation_medications())
        display_medication_category("emergencies", calculator.get_emergency_medications())
        display_medication_category("inotropes", calculator.get_inotropes())
        display_medication_category("sedation", calculator.get_sedation_paralysis())
        display_medication_category("antihypertensives", calculator.get_antihypertensives())
        display_medication_category("antiarrhythmics", calculator.get_antiarrhythmics())
        display_medication_category("others", calculator.get_others())

def display_medication_category(category_key, medications):
    """Display a category of medications in a table format"""
    if not medications:
        return
    
    # Remove subtitle for airway_defib category
    if category_key != "airway_defib":
        st.subheader(get_translation(category_key, st.session_state.language))
    
    # Check if this category has infusion medications that need rate selection
    if category_key in ['inotropes', 'sedation', 'antihypertensives', 'antiarrhythmics', 'others']:
        display_infusion_medications(medications)
    else:
        # Create DataFrame for regular medications
        df_data = []
        for med in medications:
            # Round ETT size to nearest 0.5 if it exists
            dosage = med['dosage']
            if med['name'].lower() == "ett size":
                try:
                    val = float(dosage)
                    dosage = f"{round(val * 2) / 2:.1f}"
                except:
                    pass
            
            # Propofol dosage update - convert dosage text if propofol and dosage exists
            if med['name'].lower() == "propofol":
                # replace dosage with "1-3 mg/kg" range
                dosage = "1-3 mg/kg"
            
            df_data.append({
                get_translation("medication", st.session_state.language): med['name'],
                get_translation("dosage", st.session_state.language): dosage,
                get_translation("route", st.session_state.language): med['route']
            })
        
        df = pd.DataFrame(df_data)
        
        # Use column configuration to control width
        column_config = {
            get_translation("medication", st.session_state.language): st.column_config.TextColumn(width="medium"),
            get_translation("dosage", st.session_state.language): st.column_config.TextColumn(width="medium"),
            get_translation("route", st.session_state.language): st.column_config.TextColumn(width="large")
        }
        
        st.dataframe(df, use_container_width=True, hide_index=True, column_config=column_config)
    
    st.markdown("---")

def display_infusion_medications(medications):
    """Display infusion medications with rate selection"""
    import re
    
    for i, med in enumerate(medications):
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 2])
            
            with col1:
                st.write(f"**{med['name']}**")
                st.caption(f"Weight: {med['dosage']}")
            
            with col2:
                # Extract dose range for dropdown
                if 'infusion' in med['route'].lower() or any(unit in med['route'] for unit in ['mcg/kg/min', 'mg/kg/h', 'units/kg/h']):
                    # Parse the dose range from route
                    match = re.search(r'(\d+\.?\d*)-(\d+\.?\d*)', med['route'])
                    if match:
                        min_dose = float(match.group(1))
                        max_dose = float(match.group(2))
                        
                        # Create dropdown options based on range
                        if max_dose < 1:
                            step = 0.01
                            options = [round(min_dose + i * step, 2) for i in range(int((max_dose - min_dose) / step) + 1)]
                        elif max_dose < 10:
                            step = 0.1
                            options = [round(min_dose + i * step, 1) for i in range(int((max_dose - min_dose) / step) + 1)]
                        else:
                            step = 1.0
                            options = [int(min_dose + i * step) for i in range(int((max_dose - min_dose) / step) + 1)]
                        
                        # Limit options to reasonable number
                        if len(options) > 20:
                            options = options[::len(options)//15]  # Take every nth option to get ~15 options
                        
                        selected_dose = st.selectbox(
                            "Select rate:",
                            options=options,
                            index=len(options)//2,  # Default to middle value
                            key=f"dose_{i}_{med['name']}"
                        )
                        
                        # Extract unit from route
                        unit_match = re.search(r'(mcg/kg/min|mg/kg/h|units/kg/h)', med['route'])
                        unit = unit_match.group(1) if unit_match else "units"
                        
                        with col3:
                            # Calculate actual dosage based on selected rate and weight
                            weight_kg = float(med['dosage'].split()[0])  # Extract weight from dosage string
                            
                            if 'mcg/kg/min' in unit:
                                actual_dose = selected_dose * weight_kg
                                st.metric("Actual Dose", f"{actual_dose:.1f} mcg/min")
                            elif 'mg/kg/h' in unit:
                                actual_dose = selected_dose * weight_kg
                                st.metric("Actual Dose", f"{actual_dose:.1f} mg/h")
                            elif 'units/kg/h' in unit:
                                actual_dose = selected_dose * weight_kg
                                st.metric("Actual Dose", f"{actual_dose:.2f} units/h")
                            else:
                                st.metric("Selected Rate", f"{selected_dose} {unit}")
                    else:
                        st.write(med['route'])
                else:
                    st.write(med['route'])
            
            st.markdown("---")

if __name__ == "__main__":
    main()

