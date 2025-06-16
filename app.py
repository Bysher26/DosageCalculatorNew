import streamlit as st
import pandas as pd

# Mock DosageCalculator (replace with your actual import & class)
class DosageCalculator:
    def __init__(self, weight_kg, age_years):
        self.weight_kg = weight_kg
        self.age_years = age_years

    def get_intubation_medications(self):
        return [
            {'name': 'Med A', 'dosage': '10 mg', 'route': 'IV'},
            {'name': 'Med B', 'dosage': '5 mg', 'route': 'IM'}
        ]

    def get_emergency_medications(self):
        return [
            {'name': 'Med C', 'dosage': '20 mg', 'route': 'IV'}
        ]

    # Add other medication categories methods as needed


# Language translations stub (replace with your actual translations)
def get_translation(key, lang):
    translations = {
        "weight": "Weight",
        "weight_unit": "Unit",
        "age": "Age",
        "age_unit": "Unit",
        "calculate": "Calculate",
        "patient_info": "Patient Info",
        "medication": "Medication",
        "dosage": "Dosage",
        "route": "Route",
        "intubation": "Intubation Medications",
        "emergencies": "Emergency Medications",
        "airway_defib": "AIRWAY & DEFIB"
    }
    return translations.get(key, key)


def main():
    st.title("Medical Dosage Calculator")

    # Input Weight with unit *after* number
    weight = st.number_input("Weight", min_value=0.1, max_value=300.0, value=70.0, step=0.1, format="%.1f")
    weight_unit = st.selectbox("Weight Unit", ['kg', 'lbs'], index=0)

    # Input Age with unit *after* number
    age = st.number_input("Age", min_value=0, max_value=120, value=30, step=1)
    age_unit = st.selectbox("Age Unit", ['years', 'months'], index=0)

    # Convert inputs to base units for calculation
    weight_kg = weight if weight_unit == 'kg' else weight * 0.453592
    age_years = age if age_unit == 'years' else age / 12

    calculator = DosageCalculator(weight_kg, age_years)

    if st.button(get_translation("calculate", "en")):
        st.subheader(get_translation("patient_info", "en"))
        st.write(f"{weight:.1f} {weight_unit}")
        st.write(f"{age} {age_unit}")

        # Airway & Defib section formatted with 2 columns per line
        st.markdown(f"### {get_translation('airway_defib', 'en')}")
        airway_data = [
            ("ETT size:", "#5.0 cuffed / #5.5 non-cuffed"),
            ("ETT depth:", "15.5 cm"),
            ("Laryngoscopy blade:", "2 straight or curved"),
            ("LMA size:", "2"),
            ("Defibrillation (2-4J/kg):", "26 to 52J"),
            ("Sync.Cardioversion (0.5→1→2 J/kg):", "7→13→26J")
        ]

        for label, value in airway_data:
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown(f"**{label}**")
            with col2:
                st.markdown(value)

        st.markdown("---")

        # Display Intubation Medications (example)
        st.subheader(get_translation("intubation", "en"))
        meds = calculator.get_intubation_medications()
        df = pd.DataFrame(meds)
        st.dataframe(df[['name', 'dosage', 'route']], use_container_width=True, hide_index=True)

        # You can add other medication categories similarly...

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()


