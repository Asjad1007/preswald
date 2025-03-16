from preswald import text, plotly, connect, get_df, table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Welcome message
text("# Welcome to Preswald!")
text("This is your first app. 🎉")

# Connect and load the data
connect()  # load in all sources, which by default is the sample_csv
df = get_df('viral_social_media_trends_csv')

# Check the first few rows of the data
print(df.head())

print(df.info())  
print(df.isnull().sum())  

# Filling missing values with 0
df.fillna({'Likes': 0, 'Shares': 0, 'Comments': 0}, inplace=True)  

df['Views'] = df['Views'].astype(int)
df['Likes'] = df['Likes'].astype(int)
df['Shares'] = df['Shares'].astype(int)
df['Comments'] = df['Comments'].astype(int)

sampled_df = df.sample(frac=0.1, random_state=42) 
aggregated_df = df.groupby('Platform').agg({
    'Views': 'mean',
    'Likes': 'mean',
    'Shares': 'mean',
    'Comments': 'mean',
    'Engagement_Level': lambda x: x.mode()[0]  
}).reset_index()

# scatter plot 
fig_scatter = px.scatter(
    sampled_df,  
    x='Views',
    y='Likes',
    color='Platform',
    title='Views vs Likes for Social Media Posts (Sampled Data)',
    labels={'Views': 'Views', 'Likes': 'Likes'},
    hover_data=['Region', 'Engagement_Level'],
    opacity=0.6  
)

fig_scatter.update_traces(marker=dict(size=8))

fig_scatter.update_layout(template='plotly_white')

plotly(fig_scatter)


# Hexbin Plot
if len(df) > 1000:  
    fig_hexbin = px.density_heatmap(
        df,
        x='Views',
        y='Likes',
        nbinsx=30,  
        nbinsy=30,  
        title='Density of Views vs Likes (Hexbin Plot)',
        labels={'Views': 'Views', 'Likes': 'Likes'},
        color_continuous_scale='Viridis' 
    )
    plotly(fig_hexbin)



# bar plot for average views
platform_stats = df.groupby('Platform')[['Views', 'Likes', 'Shares', 'Comments']].mean().reset_index()
fig_platform = px.bar(platform_stats, x='Platform', y='Views', color='Platform',
                      title='Average Views by Platform',
                      labels={'Platform': 'Social Media Platform', 'Views': 'Average Views'})

plotly(fig_platform)

# pie chart 
engagement_distribution = df['Engagement_Level'].value_counts().reset_index()
engagement_distribution.columns = ['Engagement_Level', 'Count']
fig_pie = px.pie(engagement_distribution, values='Count', names='Engagement_Level',
                 title='Distribution of Engagement Levels',
                 color_discrete_sequence=px.colors.qualitative.Pastel)

plotly(fig_pie)

# grouped bar chart 
engagement_metrics = df.groupby('Platform')[['Likes', 'Shares', 'Comments']].mean().reset_index()
fig_grouped_bar = go.Figure()

for metric in ['Likes', 'Shares', 'Comments']:
    fig_grouped_bar.add_trace(go.Bar(
        x=engagement_metrics['Platform'],
        y=engagement_metrics[metric],
        name=metric
    ))

fig_grouped_bar.update_layout(
    barmode='group',
    title='Average Engagement Metrics by Platform',
    xaxis_title='Platform',
    yaxis_title='Average Count',
    template='plotly_white'
)

plotly(fig_grouped_bar)

# user-controlled interactive graph (Dropdown)
metrics = ['Views', 'Likes', 'Shares', 'Comments']
fig_dropdown = go.Figure()

for metric in metrics:
    fig_dropdown.add_trace(go.Bar(
        x=df['Platform'],
        y=df[metric],
        name=metric,
        visible=(metric == 'Views') 
    ))

#  dropdown 
fig_dropdown.update_layout(
    updatemenus=[
        dict(
            buttons=[
                dict(
                    label=metric,
                    method='update',
                    args=[{'visible': [m == metric for m in metrics]},
                          {'title': f'{metric} by Platform'}]
                ) for metric in metrics
            ],
            direction='down',
            showactive=True,
            x=2.1,
            y=1.2
        )
    ],
    title='Engagement Metrics by Platform (Select Metric)',
    xaxis_title='Platform',
    yaxis_title='Count',
    template='plotly_white'
)

plotly(fig_dropdown)

table(df)