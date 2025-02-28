import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

# Генерация синтетических данных
np.random.seed(42)
n_sessions = 1000
data = {
    'session_id': range(n_sessions),
    'date': pd.date_range('2025-01-01', periods=n_sessions, freq='H'),
    'device_type': np.random.choice(['desktop', 'mobile', 'tablet'], n_sessions, p=[0.5, 0.4, 0.1]),
    'region': np.random.choice(['SPb', 'Moscow', 'Other'], n_sessions, p=[0.4, 0.4, 0.2]),
    'funnel_stage': np.random.choice(['visit', 'cart', 'paid'], n_sessions, p=[0.7, 0.2, 0.1])
}
df = pd.DataFrame(data).drop_duplicates('session_id')

# Сохранение данных в CSV-файл
if not os.path.exists('Project_1_Funnel_analysis/data'):
    os.makedirs('Project_1_Funnel_analysis/data')
df.to_csv('Project_1_Funnel_analysis/data/funnel_data.csv', index=False)
print("Первые 5 строк данных:")
print(df.head())

# Анализ общей воронки
funnel = df['funnel_stage'].value_counts().reindex(['visit', 'cart', 'paid'])
print("\nОбщая воронка:")
print(funnel)

visit_to_cart = (funnel['cart'] / funnel['visit']) * 100
cart_to_paid = (funnel['paid'] / funnel['cart']) * 100
overall_conversion = (funnel['paid'] / funnel['visit']) * 100
print(f"Конверсия visit → cart: {visit_to_cart:.1f}%")
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

# Сегментация по регионам
funnel_by_region = df.groupby(['region', 'funnel_stage']).size().unstack(fill_value=0)
funnel_by_region = funnel_by_region.reindex(columns=['visit', 'cart', 'paid'])
funnel_by_region['visit_to_cart'] = (funnel_by_region['cart'] / funnel_by_region['visit']) * 100
funnel_by_region['cart_to_paid'] = (funnel_by_region['paid'] / funnel_by_region['cart']) * 100
funnel_by_region['overall'] = (funnel_by_region['paid'] / funnel_by_region['visit']) * 100
print("\nВоронка по регионам:")
print(funnel_by_region)

# Временной анализ
df['day'] = df['date'].dt.date
time_analysis = df.groupby('day')['funnel_stage'].value_counts().unstack(fill_value=0).reindex(columns=['visit', 'cart', 'paid'])
time_analysis['conversion'] = (time_analysis['paid'] / time_analysis['visit']) * 100
print("\nКонверсия по дням:")
print(time_analysis[['conversion']].head())

# Статистический тест: (χ²) для зависимости конверсии от устройства
contingency_table = funnel_by_device[['paid', 'visit']].copy()
contingency_table['not_paid'] = contingency_table['visit'] - contingency_table['paid']
contingency_table = contingency_table[['paid', 'not_paid']]
chi2, p, dof, expected = chi2_contingency(contingency_table)
print("\n(χ²) тест зависимости конверсии от устройства:")
print(f"(χ²): {chi2:.2f}, p-value: {p:.4f}, degrees of freedom: {dof}")

# Визуализация воронки по устройствам
plt.figure(figsize=(10, 6))
for device in funnel_by_device.index:
    plt.plot(['visit', 'cart', 'paid'], funnel_by_device.loc[device, ['visit', 'cart', 'paid']], marker='o', label=device)
plt.title('Sales Funnel by Device Type')
plt.xlabel('Funnel Stage')
plt.ylabel('Number of Sessions')
plt.legend(title='Device Type')
plt.grid(True)

# Сохранение графика в файл
if not os.path.exists('Project_1_Funnel_analysis/visualizations'):
    os.makedirs('Project_1_Funnel_analysis/visualizations')

plt.savefig('Project_1_Funnel_analysis/visualizations/funnel_by_device.png')
plt.show()


# Сравнительный график конверсий
plt.figure(figsize=(12, 6))
devices = funnel_by_device.index
device_conv = funnel_by_device['overall']
plt.bar(devices, device_conv, color='skyblue', alpha=0.7, label='Device Type')
regions = funnel_by_region.index
region_conv = funnel_by_region['overall']
plt.bar(regions, region_conv, color='salmon', alpha=0.7, label='Region', width=0.4)
plt.title('Overall Conversion Rates by Device Type and Region')
plt.ylabel('Conversion Rate (%)')
plt.legend()
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.savefig('Project_1_Funnel_analysis/visualizations/conversion_comparison.png')
plt.show()

# Тепловая карта конверсий
pivot_table = df.pivot_table(index='device_type', columns='region', values='funnel_stage', 
                             aggfunc=lambda x: (x == 'paid').mean() * 100)
plt.figure(figsize=(10, 6))
sns.heatmap(pivot_table, annot=True, fmt='.1f', cmap='YlGnBu')
plt.title('Conversion Rate (%) by Device Type and Region')
plt.xlabel('Region')
plt.ylabel('Device Type')
plt.savefig('Project_1_Funnel_analysis/visualizations/heatmap_conversion.png')
plt.show()

# Временной график конверсии
plt.figure(figsize=(12, 6))
plt.plot(time_analysis.index, time_analysis['conversion'], marker='o', color='teal')
plt.title('Conversion Rate Over Time')
plt.xlabel('Date')
plt.ylabel('Conversion Rate (%)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Project_1_Funnel_analysis/visualizations/time_conversion.png')
plt.show()