# Import the required libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import os

# Import the data set
DATA_DIR = 'data'
data_path = os.path.join(DATA_DIR, 'purchase_data.csv')
df = pd.read_csv(data_path)
df['spend'] = df['price'] * df['quantitiy']
df = df[['date', 'place', 'spend']]
df = df.groupby(['date', 'place']).sum().reset_index()

# Create the Plotly figure (bar chart from the previous activity)
fig = px.bar(df, x="spend", y="date", color="place", title="Purchases by place")

# Mapbox chart
mapbox_token = "pk.eyJ1Ijoic2FyYWhzYW5kZXJzIiwiYSI6ImNrZHU5Y2hqeTI2aGYyd3R2ajVjOWVtenMifQ.EKpDFYzW2nTwiILPwecc0A"  # Go to https://www.mapbox.com/help/define-access-token/ to get your own token then add it here

px.set_mapbox_access_token(mapbox_token)

data_file = os.path.join(DATA_DIR, 'stages.csv')
df2 = pd.read_csv(data_file)

fig2 = px.scatter_mapbox(df2,
                        lat="latitude",
                        lon="longitude",
                        color="stage",
                        center=dict(lat=-23.701057, lon=-46.6970635),
                        hover_name="stage",
                        zoom=14.5,
                        title='Lollapalooza Brazil 2018 map')

# Create a Dash app (if you use a stylesheet in the assets folder you will need to use __name__ in the constructor).
app = dash.Dash(__name__)

# Create the app layout and add the bar chart to it
app.layout = html.Div(children=[

    html.H1('Lollapalooza experience'),

    dcc.Graph(figure=fig),

    html.H2('Where did I go during the festival?'),

    dcc.Graph(figure=fig2)
])

# Run the web app server
if __name__ == '__main__':
    app.run_server(debug=False, port=8050)
