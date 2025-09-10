import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# Чтение данных из CSV
df = pd.read_csv('defects.csv')

# Сортировка по убыванию числа дефектов
df = df.sort_values(by='Число дефектов', ascending=False).reset_index(drop=True)

# Объединение редких дефектов в "Прочие" (оставляем топ-5, остальные в "Прочие")
top_n = 5
main_defects = df.iloc[:top_n]
other_defects = df.iloc[top_n:]
other_row = pd.DataFrame({
    'Типы дефектов': ['Прочие'],
    'Число дефектов': [other_defects['Число дефектов'].sum()]
})
df = pd.concat([main_defects, other_row], ignore_index=True)

# Расчет процентов и накопленного процента
total_defects = df['Число дефектов'].sum()
df['Процент'] = df['Число дефектов'] / total_defects * 100
df['Накопленный процент'] = df['Процент'].cumsum()

# Построение диаграммы Парето
fig, ax1 = plt.subplots(figsize=(10, 6))

# Столбики для процентов
ax1.bar(df['Типы дефектов'], df['Процент'], color='b', alpha=0.7)
ax1.set_xlabel('Типы дефектов')
ax1.set_ylabel('Процент дефектов', color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.yaxis.set_major_formatter(PercentFormatter())

# Кумулятивная линия
ax2 = ax1.twinx()
ax2.plot(df['Типы дефектов'], df['Накопленный процент'], color='r', marker='o')
ax2.set_ylabel('Накопленный процент', color='r')
ax2.tick_params(axis='y', labelcolor='r')
ax2.yaxis.set_major_formatter(PercentFormatter())

# Линии для ABC-анализа
ax2.axhline(80, color='g', linestyle='--', label='80% (A/B)')
ax2.axhline(95, color='purple', linestyle='--', label='95% (B/C)')
ax2.legend()

# Настройка графика
plt.title('Диаграмма Парето для дефектов 6-осевого робота-манипулятора')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Сохранение графика
plt.savefig('pareto_diagram.png')
plt.show()