import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')
print(df.head())

# Add 'overweight' column
# weight in kilograms by the square of their height in meters.
df['overweight'] = (df['weight'] / (df['height']/100)**2).apply(lambda x: 1 if x > 25 else 0)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0.
# If the value is more than 1, make the value 1.
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat['total'] = 1
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).count()


    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(x='variable', y='total', data=df_cat, hue='value', kind='bar', col='cardio')



    # Get the figure for the output
    fig = plt.gcf()


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    filter1 = df['ap_lo'] <= df['ap_hi']
    filter2 = df['height'] >= df['height'].quantile(0.025)
    filter3 = df['height'] <= df['height'].quantile(0.975)
    filter4 = df['weight'] >= df['weight'].quantile(0.025)
    filter5 = df['weight'] <= df['weight'].quantile(0.975)

    df_heat = df[filter1 & filter2 & filter3 & filter4 & filter5]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(11,9))

    # Draw the heatmap with 'sns.heatmap()'
    ax = sns.heatmap(corr, vmax=.3, center=0, annot=True, fmt=".1f", linewidths=.5,
        cbar_kws={"shrink": 0.5, "ticks": [-0.08, 0.00, 0.08, 0.16, 0.24], "orientation": "vertical"},
        square=True, mask=mask, ax=ax)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
