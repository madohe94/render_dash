import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)

# Load the CSV data for the second graph
csv_url = "https://raw.githubusercontent.com/madohe94/TS/main/join_surprise_spotify.csv"
df = pd.read_csv(csv_url)

# Load the data from the provided CSV URL for the first graph
url2 = "https://raw.githubusercontent.com/madohe94/TS/ebbeb46d3d68ab0e0ade2cf0af82b31c083a1c46/spoti_join_setlist.csv"
alll = pd.read_csv(url2)
surprise = alll[alll['surprise'] == 'surprise song']
surprise_grouped = surprise.groupby(['date', 'Album']).size().unstack(fill_value=0)

# Custom album-color mapping
album_color_mapping = {
    'Lover': 'pink',
    "Speak Now (Taylor's Version)": 'darkviolet',
    "Red (Taylor's Version)": 'red',
    "1989 (Deluxe)": 'blue',
    "Fearless (Taylor's Version)": 'goldenrod',
    "Midnights (The Til Dawn Edition)": 'rebeccapurple',
    "evermore (deluxe version)": 'darkorange',
    "folklore (deluxe version)": 'grey',
    "reputation": 'black',
    "Taylor Swift": 'green',
    'Other': 'blue'
}

# Define album colors
album_colors = {
    'Lover': 'pink',
    "Speak Now (Taylor's Version)": 'darkviolet',
    "Red (Taylor's Version)": 'red',
    "1989 (Deluxe)": 'blue',
    "Fearless (Taylor's Version)": 'goldenrod',
    "Red (Taylor's Version)": 'red',
    "Midnights (The Til Dawn Edition)": 'rebeccapurple',
    "evermore (deluxe version)": 'darkorange',
    "folklore (deluxe version)": 'grey',
    "reputation": 'black'
    # Add more albums and colors as needed
}

# Get the colors for each album based on the dictionary
colors = [album_colors.get(album, 'grey') for album in surprise_grouped.columns]

# Define the order of albums for consistent column widths
album_order = [
    "Other",
    "Taylor Swift",
    "Fearless (Taylor's Version)",
    "Speak Now (Taylor's Version)",
    "Red (Taylor's Version)",
    "1989 (Deluxe)",
    "reputation",
    'Lover',
    "evermore (deluxe version)",
    "folklore (deluxe version)",
    "Midnights (The Til Dawn Edition)"
]

# Add a new column with all integer values (1)
df['value'] = 1

# Step 3: Create a grouped Plotly Express bar chart with 'surprise' column divisions
def update_grouped_bar_chart(selected_surprise):
    filtered_df = df[df['surprise'] == selected_surprise]
    fig = px.bar(filtered_df, x='Album', y='value', color='Album', barmode='group',
                 color_discrete_map=album_color_mapping, facet_col='surprise',
                 category_orders={"Album": album_order},
                 text='song', hover_name='song', hover_data={'value': False, 'song': False, 'Album': False})
    fig.update_layout(title_x=0.5, width=5000)
    fig.update_layout(showlegend=False)
    fig.update_layout(bargap=0)
    fig.update_xaxes(fixedrange=True, range=[-0.5, len(album_order) - 0.5])
    fig.update_yaxes(fixedrange=True)
    return fig

# Plotly figure for the second graph
fig2 = px.bar(surprise_grouped, x=surprise_grouped.index, y=surprise_grouped.columns,
              title='Surprise Songs by Album, Stacked by Date',
              labels={'x': 'Date', 'y': 'Number of Songs'}, color_discrete_sequence=colors)
fig2.update_layout(title_x=0.5, width=5000)
fig2.update_layout(showlegend=False)
fig2.update_layout(bargap=0)
fig2.update_xaxes(fixedrange=True)
fig2.update_yaxes(fixedrange=True)

# Create the layout
app.layout = html.Div([
    html.Div([
        html.H1("The Eras Tour Song Breakdown", style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='surprise-dropdown',
            options=[{'label': surprise, 'value': surprise} for surprise in df['surprise'].unique()],
            value=df['surprise'].unique()[0],
            multi=False
        ),
        dcc.Graph(
            id='grouped-bar-chart',
            config={'scrollZoom': False},
            style={'width': '100%', 'height': '80vh'}
        )
    ], className="six columns"),
    html.Div([
        dcc.Graph(id='surprise-graph', figure=fig2),
        html.Br(),
        html.P("If you find this dashboard useful, consider supporting me by buying me a coffee!"),
        html.A("Buy Me a Coffee", href="https://www.buymeacoffee.com/madohe794", target="_blank")
    ], className="six columns")
], className="row")

# Callback to update the grouped bar chart
@app.callback(
    Output('grouped-bar-chart', 'figure'),
    [Input('surprise-dropdown', 'value')]
)
def update_chart(selected_surprise):
    return update_grouped_bar_chart(selected_surprise)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
