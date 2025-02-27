import pandas as pd
import numpy as np
import os

# Генерация синтетических данных
np.random.seed(42)  # Для воспроизводимости
n_sessions = 1000
data = {
    'session_id': range(n_sessions),
    'date': pd.date_range('2025-01-01', periods=n_sessions, freq='H'),
    'device_type': np.random.choice(['desktop', 'mobile', 'tablet'], n_sessions, p=[0.5, 0.4, 0.1]),
    'region': np.random.choice(['SPb', 'Moscow', 'Other'], n_sessions, p=[0.4, 0.4, 0.2]),
    'funnel_stage': np.random.choice(['visit', 'cart', 'paid'], n_sessions, p=[0.7, 0.2, 0.1])
}
df = pd.DataFrame(data).drop_duplicates('session_id')

# Сохранение данных (опционально)

os.makedirs('Project_1_Funnel_Analysis/data', exist_ok=True)

df.to_csv('Project_1_Funnel_Analysis/data/funnel_data.csv', index=False)
print("Первые 5 строк данных:")
print(df.head())