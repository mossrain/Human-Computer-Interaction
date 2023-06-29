import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objects as go
from preprocess import *
import plotly.express as px

cnt_list = ['Category', 'Type', 'Size', 'Rating', 'Content Rating']
top_list = ['Top 20 Reviews', 'Top 20 Installs', 'Top 20 Ratings',  'Top 20 Prices']

cat_cnt = category_count()
type_cnt = type_count()
size_cnt = size_count()
rat_cnt = rating_count()
age_cnt = content_rating_count()

df_rat = topk('Rating')
df_ins = topk('Installs')
df_rev = topk('Reviews')
df_pri = topk('Price')

time_df = update_time_data()

df = get_data()

app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1(children='Google Play Store Apps', style={'textAlign': 'center'}),
    html.Br(),

    # 第一个下拉框和饼状图
    html.Div([
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': i, 'value': i} for i in cnt_list],
            value=cnt_list[0]  # Default selection
        ),
        dcc.Graph(id='pie-chart')
    ], style={'display': 'inline-block', 'width': '50%'}),

    # 第二个下拉框和折线图
    html.Div([
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': category, 'value': category} for category in time_df['Category'].unique()],
            value='ALL'
        ),
        dcc.Graph(id='line-chart')
    ], style={'display': 'inline-block', 'width': '50%'}),

    # 第三和第四个下拉框和柱状图
    html.Div([
        dcc.Dropdown(
            id='dropdown-data',
            options=[{'label': i, 'value': i} for i in top_list],
            value=top_list[0]  # Default selection
        ),
       
        
    ], style={'display': 'inline-block', 'width': '50%'}),

    html.Div([
         dcc.Dropdown(
            id='dropdown-category',
            options=[{'label': i, 'value': i} for i in cat_cnt.index],
            value=cat_cnt.index[0]  # Default selection
        ),
    ], style={'display': 'inline-block', 'width': '50%', 'float': 'right'}),

    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='scatter-3d')
])


@app.callback(
    dash.dependencies.Output('pie-chart', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')]
)
def update_pie_chart(selected_value):
    selected_series = None
    if selected_value == 'Category':
        selected_series = cat_cnt
    elif selected_value == 'Type':
        selected_series = type_cnt
    elif selected_value == 'Size':
        selected_series = size_cnt
    elif selected_value == 'Rating':
        selected_series = rat_cnt
    elif selected_value == 'Content Rating':
        selected_series = age_cnt

    labels = selected_series.index
    values = selected_series.values
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title=f"Number of apps in each {selected_value}")

    return fig

@app.callback(
    dash.dependencies.Output('line-chart', 'figure'),
    [dash.dependencies.Input('category-dropdown', 'value')]
)
def update_line_chart(selected_category):
    filtered_df = time_df[time_df['Category'] == selected_category]
    filtered_df = filtered_df.groupby('Year').first().reset_index()
    fig = go.Figure(data=go.Scatter(x=filtered_df['Year'], y=filtered_df['Number'], mode='lines'))
    fig.update_layout(title=f"Number of Apps updated each year in Category: {selected_category}")
    return fig

@app.callback(
    dash.dependencies.Output('bar-chart', 'figure'),
     [dash.dependencies.Input('dropdown-data', 'value'),
     dash.dependencies.Input('dropdown-category', 'value')]
)
def update_bar_chart(selected_data, selected_category):
    if selected_data == 'Top 20 Ratings':
        selected_df = df_rat
    elif selected_data == 'Top 20 Installs':
        selected_df = df_ins
    elif selected_data == 'Top 20 Reviews':
        selected_df = df_rev
    elif selected_data == 'Top 20 Prices':
        selected_df = df_pri


    filtered_df = selected_df[selected_df['Category'] == selected_category]
    # print(filtered_df)

    fig = go.Figure(data=go.Bar(x=filtered_df['App'], y=filtered_df['Number'].astype(float)))
    fig.update_layout(title=f"{selected_data} in Category: {selected_category}")

    # if selected_data == 'Top 20 Ratings':
    #     fig.update_yaxes(range=[4.5,5.0])

    return fig

@app.callback(
    dash.dependencies.Output('scatter-3d', 'figure'),
    [dash.dependencies.Input('scatter-3d', 'id')]
)
def update_scatter_3d(id):
    # Create the 3D scatter plot figure
    fig = px.scatter_3d(df, x='Last Updated', y='Rating', z='Category', 
                        size='Installs', color='Reviews', color_continuous_scale='RdYlBu_r',
                        hover_data=['App'])
    fig.update_layout(title='3D Scatter Plot of Apps(size for Installs, color for Reviews)')

    # Set the axis labels
    fig.update_layout(scene=dict(
        xaxis=dict(title='Last Updated'),
        yaxis=dict(title='Rating'),
        zaxis=dict(title='Category')
    ))

    # # 把fig的面积调大一点
    fig.update_layout(width=1200, height=800)


    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
