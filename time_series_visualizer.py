from calendar import calendar
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import calendar

df=pd.read_csv("fcc-forum-pageviews.csv")
print(df)

df_top=df["value"].quantile(0.975)
df_low=df["value"].quantile(0.025)
df_cleaned = df[(df['value'] >= df_low) & (df['value'] <= df_top)]
print(df_cleaned)

def draw_line_plot():
    x_axis=np.array(df["date"])
    y_axis=np.array(df["value"])
    plt.figure(figsize=(12,6))
    plt.plot(x_axis, y_axis, label='Page Views')
    plt.axhline(y=df_top, color='r', linestyle='--', label='Top 2.5%')
    plt.axhline(y=df_low, color='g', linestyle='--', label='Bottom 2.5%')
    plt.title('Daily FreeCodeCamp Forum Page Views')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.legend()
    plt.show()
draw_line_plot()

def draw_bar_plot():
    df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')
    df = df[
        (df['value'] >= df['value'].quantile(0.025)) &
        (df['value'] <= df['value'].quantile(0.975))
    ]

    # Extract year and month number
    df['year'] = df.index.year
    df['month'] = df.index.month

    # Group by year and month, calculate mean
    df_grouped = df.groupby(['year', 'month'])['value'].mean().unstack()

    # Rename columns from month number to month name
    df_grouped.columns = [calendar.month_name[i] for i in df_grouped.columns]

    # Reorder columns to proper month order
    month_order = list(calendar.month_name)[1:]  # skip empty string at index 0
    df_grouped = df_grouped[month_order]

    # Plot
    fig = df_grouped.plot(kind='bar', figsize=(15, 8)).figure

    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")
    plt.tight_layout()
    plt.show()
draw_bar_plot()    

def draw_box_plot():
    df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')
    df = df[
        (df['value'] >= df['value'].quantile(0.025)) &
        (df['value'] <= df['value'].quantile(0.975))
    ]
    df["value"] = pd.to_datetime(df["value"], errors='coerce')
    df['year'] = df['value'].dt.year
    df['month'] = df['value'].dt.strftime('%b')       # e.g., 'Jan', 'Feb'
    df['month_num'] = df['value'].dt.month            # used for ordering

    # Sort by month_num to ensure correct month order
    df = df.sort_values('month_num')

    # Draw box plots using seaborn
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Year-wise box plot
    sns.boxplot(x='year', y='value', data=df, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise box plot
    sns.boxplot(x='month', y='value', data=df, ax=axes[1],
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    plt.tight_layout()
    plt.show()
draw_box_plot()
