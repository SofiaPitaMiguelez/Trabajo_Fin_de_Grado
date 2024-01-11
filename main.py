import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from app import app as app_layout
from map_app import map_app as map_app_layout
#from assets import style
main = dash.Dash(__name__, suppress_callback_exceptions=True)

# Layout de la nueva vista con dos botones
new_view_layout = html.Div([
    html.H1("Página Principal", style={'font-weight': 'bold'}),
    html.H2("A continuación, puedes seleccionar la vista a la que quieres acceder:"),
    dcc.Link("- Gráficas generadas sobre el ICA y los agentes contaminantes", href="/app"),
    html.H3("Donde podrás visualizar cuales son los agentes más contaminantes en ciertos puntos temporales y espaciales, así como la evolución del Índice de Calidad del Aire (ICA) medida por un sensor a lo largo del mes que selecciones"),
    html.Br(),
    html.Br(),
    dcc.Link("- Visualización del mapa del área en estudio", href="/map_app"),
    html.H3("Donde podrás ver como evolucionan los valores de ICA en diferentes puntos del área de estudio a lo largo del periodo de tiempo que escojas. Además, podrás decidir si quieres que la información esté desagregada o sigua algún tipo de agrupación")
], style={'color': 'white', 'margin': '100px'} )

main.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id="page-content"),
    #html.Div(id="new-view-content", children=new_view_layout)  # Agrega la nueva vista al layout principal
])

@main.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/app":
        return app_layout.layout
    elif pathname == "/map_app":
        return map_app_layout.layout
    else:
        return new_view_layout
        
if __name__ == "__main__":
    main.run_server(debug=True)

