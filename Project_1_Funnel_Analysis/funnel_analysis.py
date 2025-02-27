import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

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

# Анализ общей воронки
funnel = df['funnel_stage'].value_counts().reindex(['visit', 'cart', 'paid'])
print("Общая воронка:")
print(funnel)

# Конверсии
visit_to_cart = (funnel['cart'] / funnel['visit']) * 100
cart_to_paid = (funnel['paid'] / funnel['cart']) * 100
overall_conversion = (funnel['paid'] / funnel['visit']) * 100
print(f"\nКонверсия visit → cart: {visit_to_cart:.1f}%")
print(f"Конверсия cart → paid: {cart_to_paid:.1f}%")
print(f"Общая конверсия: {overall_conversion:.1f}%")

# Сегментация по устройствам
funnel_by_device = df.groupby(['device_type', 'funnel_stage']).size().unstack(fill_value=0)
funnel_by_device = funnel_by_device.reindex(columns=['visit', 'cart', 'paid'])
funnel_by_device['visit_to_cart'] = (funnel_by_device['cart'] / funnel_by_device['visit']) * 100
funnel_by_device['cart_to_paid'] = (funnel_by_device['paid'] / funnel_by_device['cart']) * 100
funnel_by_device['overall'] = (funnel_by_device['paid'] / funnel_by_device['visit']) * 100
print("\nВоронка по устройствам:")
print(funnel_by_device)

# Визуализация воронки по устройствам
devices = funnel_by_device.index
stages = ['visit', 'cart', 'paid']
colors = ['#FF9999', '#66B2FF', '#99FF99']

os.makedirs('Project_1_Funnel_Analysis/visualizations', exist_ok=True)

plt.figure(figsize=(10, 6))
for i, device in enumerate(devices):
    plt.plot(stages, funnel_by_device.loc[device, stages], marker='o', label=device, color=colors[i])


plt.title('Sales Funnel by Device Type')
plt.xlabel('Funnel Stage')
plt.ylabel('Number of Sessions')
plt.legend(title='Device Type')
plt.grid(True)
plt.savefig('Project_1_Funnel_Analysis/visualizations/funnel.png')
plt.show()