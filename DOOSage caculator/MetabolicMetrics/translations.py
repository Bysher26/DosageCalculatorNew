# Translation dictionary for English and Arabic
TRANSLATIONS = {
    'en': {
        'title': '💊 Medical Dosage Calculator',
        'subtitle': 'Calculate medication dosages based on patient weight and age',
        'weight_unit': 'Unit',
        'weight': 'Weight',
        'age_unit': 'Unit',
        'age': 'Age',
        'calculate': 'Calculate Dosages',
        'patient_info': 'Patient Information',
        'years': 'years',
        'months': 'months',
        'medication': 'Medication',
        'dosage': 'Dosage',
        'route': 'Route/Notes',
        'notes': 'Additional Notes',
        'weight_error': 'Please enter a valid weight greater than 0',
        'age_error': 'Please enter a valid age',
        
        # Categories
        'airway_defib': 'AIRWAY & DEFIB',
        'intubation': 'INTUBATION MEDICATIONS',
        'emergencies': 'EMERGENCIES',
        'inotropes': 'INOTROPES',
        'sedation': 'SEDATION & PARALYSIS',
        'antihypertensives': 'ANTI-HYPERTENSIVES',
        'antiarrhythmics': 'ANTI-ARRHYTHMICS',
        'others': 'OTHERS'
    },
    'ar': {
        'title': '💊 حاسبة جرعات الأدوية الطبية',
        'subtitle': 'احسب جرعات الأدوية بناءً على وزن وعمر المريض',
        'weight_unit': 'الوحدة',
        'weight': 'الوزن',
        'age_unit': 'الوحدة',
        'age': 'العمر',
        'calculate': 'احسب الجرعات',
        'patient_info': 'معلومات المريض',
        'years': 'سنوات',
        'months': 'أشهر',
        'medication': 'الدواء',
        'dosage': 'الجرعة',
        'route': 'طريقة الإعطاء/ملاحظات',
        'notes': 'ملاحظات إضافية',
        'weight_error': 'يرجى إدخال وزن صحيح أكبر من صفر',
        'age_error': 'يرجى إدخال عمر صحيح',
        
        # Categories
        'airway_defib': 'الممرات الهوائية وإزالة الرجفان',
        'intubation': 'أدوية التنبيب',
        'emergencies': 'حالات الطوارئ',
        'inotropes': 'الأدوية المقوية للقلب',
        'sedation': 'التهدئة والشلل',
        'antihypertensives': 'خافضات ضغط الدم',
        'antiarrhythmics': 'مضادات اضطراب النظم',
        'others': 'أخرى'
    }
}

LANGUAGES = {
    'en': 'English',
    'ar': 'العربية'
}

def get_translation(key, language='en'):
    """Get translation for a given key and language"""
    return TRANSLATIONS.get(language, {}).get(key, TRANSLATIONS['en'].get(key, key))
