import dash
from dash import html
from dash import dcc
from dash import Input, Output

from main import main_layout, main_callbacks, app
from app import app_layout
from app_instance import app_instance, app_instance_callbacks

#app = dash.Dash(__name__, suppress_callback_exceptions=True)

# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div(id='page-content')
# ])

# Define callback to update page content based on URL
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/app_instance':
        return app_layout
        #return app_instance.layout()
    else:
        return main_layout()

# Combine all callbacks
main_callbacks(app)
app_instance_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
