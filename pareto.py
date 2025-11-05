import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# Чтение данных из CSV
df = pd.read_csv('defects.csv')

# Сортировка по убыванию числа дефектов
df = df.sort_values(by='Число дефектов', ascending=False).reset_index(drop=True)

# Объединение редких дефектов в "Прочие" (увеличили top_n до 10 для показа большего количества столбцов)
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

# Построение диаграммы Парето (увеличили ширину фигуры для лучшей видимости большего количества столбцов)
fig, ax1 = plt.subplots(figsize=(15, 6))

# Столбики для процентов
ax1.bar(df['Типы дефектов'], df['Процент'], color='b', alpha=0.7)
ax1.set_xlabel('Типы дефектов')
ax1.set_ylabel('Процент дефектов', color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.yaxis.set_major_formatter(PercentFormatter())
# Поворот подписей по оси X на 45 градусов для лучшей читаемости
plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

# Кумулятивная линия
ax2 = ax1.twinx()
ax2.plot(df['Типы дефектов'], df['Накопленный процент'], color='r', marker='o')
ax2.set_ylabel('Накопленный процент', color='r')
ax2.tick_params(axis='y', labelcolor='r')
ax2.yaxis.set_major_formatter(PercentFormatter())

# Горизонтальные линии для ABC-анализа
ax2.axhline(80, color='g', linestyle='--', label='80% (A/B)')
ax2.axhline(95, color='purple', linestyle='--', label='95% (B/C)')
ax2.legend()

# Добавление вертикальных разделителей для групп ABC
# Находим позиции (индексы), где накопленный процент впервые превышает пороги
a_end = df[df['Накопленный процент'] >= 60].index[0] + 0.5  # Граница A/B
b_end = df[df['Накопленный процент'] >= 80].index[0] + 0.5  # Граница B/C

# Рисуем вертикальные линии
ax1.axvline(x=a_end, color='g', linestyle='--', label='Граница A/B')
ax1.axvline(x=b_end, color='purple', linestyle='--', label='Граница B/C')

# Добавляем подписи групп A, B, C под осью X
a_mid = a_end / 2
b_mid = a_end + (b_end - a_end) / 2
c_mid = b_end + (len(df) - b_end) / 2
ax1.text(a_mid, -5, 'Группа A', ha='center', va='top', fontsize=10, color='g')
ax1.text(b_mid, -5, 'Группа B', ha='center', va='top', fontsize=10, color='purple')
ax1.text(c_mid, -5, 'Группа C', ha='center', va='top', fontsize=10, color='black')


plt.subplots_adjust(bottom=0.25)

plt.title('Диаграмма Парето для дефектов 6-осевого робота-манипулятора')

# Дополнительная настройка расположения, чтобы повернутые подписи не обрезались
plt.tight_layout()


# Сохранение графика
plt.savefig('pareto_diagram_with_abc.png')
plt.show()