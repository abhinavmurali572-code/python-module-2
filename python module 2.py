# Module 1 End Project - ABC Company Analysis
# Total: 458 rows, 9 columns

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for better graphs
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10,6)

# 1. LOAD DATASET
# Replace with your file name
df = pd.read_csv('ABC_Employees.csv')  # or pd.read_excel if xlsx
print(f"Shape: {df.shape}")
print(df.head())
print(df.info())
print(df.describe())

# ================= PREPROCESSING (1 Mark) =================
# Correct height column with random numbers 150-180
np.random.seed(42)  # for reproducibility
df['height'] = np.random.randint(150, 181, size=len(df))

# Check for nulls / duplicates - ensure consistency
print("Null values:\n", df.isnull().sum())
df = df.drop_duplicates()
df = df.dropna() # if any

# Check columns (assuming: Team, Position, Age, Salary, Height etc.)
print("Columns:", df.columns.tolist())

# ================= ANALYSIS TASK 1 (2 Marks + 2 Graph) =================
# Distribution of employees across each team + percentage
team_counts = df['Team'].value_counts()
team_perc = df['Team'].value_counts(normalize=True) * 100

team_summary = pd.DataFrame({
    'Count': team_counts,
    'Percentage': team_perc.round(2)
})
print(team_summary)

# Visualization 1
plt.figure()
team_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Distribution of Employees Across Teams', fontsize=14, fontweight='bold')
plt.xlabel('Team')
plt.ylabel('Number of Employees')
plt.xticks(rotation=45)
plt.show()

plt.figure()
plt.pie(team_counts, labels=team_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Percentage Split of Employees by Team')
plt.show()

# ================= ANALYSIS TASK 2 (2 Marks + 2 Graph) =================
# Segregate employees based on their positions
position_counts = df['Position'].value_counts()
print(position_counts)

plt.figure()
sns.countplot(y='Position', data=df, order=position_counts.index, palette='viridis')
plt.title('Employees Segregated by Position')
plt.xlabel('Count')
plt.show()

plt.figure()
position_counts.plot(kind='barh', color='coral')
plt.title('Position-wise Employee Distribution')
plt.show()

# ================= ANALYSIS TASK 3 (2 Marks + 2 Graph) =================
# Predominant age group
# Create age bins
bins = [0, 25, 35, 45, 55, 100]
labels = ['<25', '25-35', '35-45', '45-55', '55+']
df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels)

age_group_counts = df['Age_Group'].value_counts().sort_index()
print("Predominant Age Group:", age_group_counts.idxmax(), "with", age_group_counts.max(), "employees")

plt.figure()
sns.histplot(df['Age'], bins=15, kde=True, color='green')
plt.title('Age Distribution of Employees')
plt.xlabel('Age')
plt.show()

plt.figure()
age_group_counts.plot(kind='bar', color='orange', edgecolor='black')
plt.title('Predominant Age Group Among Employees')
plt.xlabel('Age Group')
plt.ylabel('Count')
plt.show()

# ================= ANALYSIS TASK 4 (2 Marks + 2 Graph) =================
# Which team and position have highest salary expenditure
team_salary = df.groupby('Team')['Salary'].sum().sort_values(ascending=False)
position_salary = df.groupby('Position')['Salary'].sum().sort_values(ascending=False)

print("Team with highest salary expenditure:", team_salary.idxmax())
print(team_salary)
print("\nPosition with highest salary expenditure:", position_salary.idxmax())
print(position_salary)

plt.figure()
team_salary.plot(kind='bar', color='teal')
plt.title('Total Salary Expenditure by Team')
plt.ylabel('Total Salary')
plt.xticks(rotation=45)
plt.show()

plt.figure()
sns.barplot(x=position_salary.values, y=position_salary.index, palette='mako')
plt.title('Total Salary Expenditure by Position')
plt.xlabel('Total Salary')
plt.show()

# ================= ANALYSIS TASK 5 (2 Marks + 2 Graph) =================
# Correlation between Age and Salary
correlation = df['Age'].corr(df['Salary'])
print(f"Correlation between Age and Salary: {correlation:.3f}")

plt.figure()
sns.scatterplot(x='Age', y='Salary', data=df, hue='Team', alpha=0.7)
plt.title(f'Age vs Salary Correlation (r={correlation:.2f})')
plt.show()

plt.figure()
sns.regplot(x='Age', y='Salary', data=df, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title('Age vs Salary - Regression Plot')
plt.show()

# ================= DATA STORY / INSIGHTS (3 Marks) =================
print("""
INSIGHTS:
1. The largest team is {0} with {1:.1f}% of total staff.
2. Most common position is {2}.
3. Dominant age group is {3}, indicating a {4} workforce.
4. Highest salary spending is on Team {5} and Position {6}.
5. Age-Salary correlation is {7:.2f} - {'positive' if correlation>0 else 'negative'} relation, meaning {'older employees tend to earn more' if correlation>0.3 else 'no strong relation'}.
""".format(
    team_summary.index[0], team_summary['Percentage'].iloc[0],
    position_counts.idxmax(),
    age_group_counts.idxmax(), "young" if age_group_counts.idxmax() in ['<25','25-35'] else "mature",
    team_salary.idxmax(), position_salary.idxmax(), correlation
))
