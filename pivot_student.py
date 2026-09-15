from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent

with sqlite3.connect((ROOT / 'data' / 'warehouse.db').as_uri() + '?mode=ro', uri=True) as con:
    df = pd.read_sql_query('SELECT * FROM sales', con)

print(df.head())

# P1: province x month, sum(amount), fill_value=0, margins=True
p1 = pd.pivot_table(
    df,
    index='province',
    columns='month',
    values='amount',
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='Total',
)
print('\nP1 (province x month):')
print(p1)
p1.to_csv(ROOT / 'pivot_province_month.csv')

# P2: filter September, then category x province
sep_df = df[df['month'] == '2026-09']
p2 = pd.pivot_table(
    sep_df,
    index='category',
    columns='province',
    values='amount',
    aggfunc='sum',
)
print('\nP2 (September: category x province):')
print(p2)
p2.to_csv(ROOT / 'pivot_september.csv')

# P3: assert Grand Total of P1 equals df['amount'].sum()
grand_total = p1.loc['Total', 'Total']
assert grand_total == df['amount'].sum(), (
    f'Grand total mismatch: pivot={grand_total}, raw sum={df["amount"].sum()}'
)
print(f'\nAssert passed: P1 Grand Total ({grand_total}) == df["amount"].sum() ({df["amount"].sum()})')

# Error experiment: pivot without aggfunc (defaults to mean) to show why Bangkok/Sep gives 270
p1_default = pd.pivot_table(
    df,
    index='province',
    columns='month',
    values='amount',
    fill_value=0,
)
print('\nWithout aggfunc (defaults to mean):')
print(p1_default)
print('Bangkok / 2026-09 mean value:', p1_default.loc['Bangkok', '2026-09'])
# Bangkok September rows are O1005 (300) and O1006 (240) -> mean = (300+240)/2 = 270
# This is the AVERAGE per line, not the total revenue.

# P4: export each result to CSV in the submission folder (P1/P2 already exported above)
p1_default.to_csv(ROOT / 'pivot_province_month_mean_demo.csv')
