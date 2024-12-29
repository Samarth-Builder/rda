import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from datetime import datetime

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>RDA Calculator</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Russo+One&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
            
            body {
                background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
                color: #fff;
                font-family: 'Inter', sans-serif;
                height: 100vh;
                margin: 0;
                padding: 0;
                overflow: hidden;
            }
            
            .main-container {
                background: rgba(0, 0, 0, 0.7);
                border: 2px solid #ff0000;
                border-radius: 15px;
                box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
                padding: 20px;
                margin: 10px;
                height: calc(100vh - 20px);
                backdrop-filter: blur(10px);
            }
            
            .neon-text {
                color: #fff;
                text-shadow: 0 0 5px #fff,
                            0 0 10px #ff0000,
                            0 0 20px #ff0000;
                font-family: 'Inter', sans-serif;
                letter-spacing: 1px;
            }
            
            .neon-button {
                background: linear-gradient(45deg, #ff0000, #ff4d4d);
                color: #fff;
                border: none;
                padding: 8px 20px;
                border-radius: 8px;
                transition: all 0.3s ease;
                text-transform: uppercase;
                font-weight: bold;
                box-shadow: 0 0 15px rgba(255, 0, 0, 0.5);
                font-family: 'Inter', sans-serif;
                letter-spacing: 1px;
            }
            
            .neon-button:hover {
                background: linear-gradient(45deg, #ff4d4d, #ff0000);
                box-shadow: 0 0 25px rgba(255, 0, 0, 0.8);
                transform: scale(1.05);
            }
            
            .history-item {
                background: linear-gradient(90deg, #1a1a1a, #2a2a2a);
                border-left: 4px solid #ff0000;
                margin: 5px 0;
                padding: 10px;
                border-radius: 0 8px 8px 0;
                animation: slideIn 0.3s ease-out;
            }
            
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            
            .fraction {
                font-size: 24px;
                display: inline-block;
                vertical-align: middle;
                text-align: center;
                margin: 10px 0;
                width: 100%;
                background: rgba(0, 0, 0, 0.3);
                padding: 15px;
                border-radius: 15px;
            }
            
            .fraction-line {
                height: 3px;
                background: linear-gradient(90deg, #ff0000, #00ff00);
                margin: 10px 0;
                border-radius: 2px;
                box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
            }
            
            .brand-signature {
                font-family: 'Russo One', sans-serif;
                background: linear-gradient(45deg, #00ff00, #00cc00);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 20px;
                padding: 8px 15px;
                border-radius: 8px;
                border: 2px solid #00ff00;
                animation: glow 2s infinite alternate;
                box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
                white-space: nowrap;
            }
            
            @keyframes glow {
                from { text-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00; }
                to { text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00; }
            }

            .input-label {
                color: #00ff00;
                font-size: 14px;
                margin-bottom: 5px;
                text-transform: uppercase;
                letter-spacing: 1px;
                text-shadow: 0 0 5px rgba(0, 255, 0, 0.5);
            }

            .input-box {
                background: rgba(26, 26, 26, 0.9);
                border: 2px solid #ff0000;
                color: #fff;
                padding: 8px;
                border-radius: 8px;
                width: 100%;
                font-family: 'Inter', sans-serif;
                transition: all 0.3s ease;
            }

            .input-box:focus {
                border-color: #00ff00;
                box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
                outline: none;
            }

            .input-group { margin-bottom: 15px; }

            .result-display {
                font-size: 28px;
                margin: 10px 0;
                padding: 10px;
                background: rgba(0, 0, 0, 0.5);
                border-radius: 10px;
            }

            .history-section {
                background: rgba(0, 0, 0, 0.5);
                border-radius: 15px;
                padding: 15px;
                height: calc(100% - 60px);
                overflow-y: auto;
            }

            .history-title {
                border-bottom: 2px solid #ff0000;
                padding-bottom: 10px;
                margin-bottom: 15px;
            }
            
            #history-list {
                max-height: calc(100vh - 250px);
                overflow-y: auto;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# App layout
app.layout = html.Div([
    dbc.Container([
        html.Div([
            # Title
            html.H1("RDA Calculator", className="text-center neon-text mt-2 mb-3"),
            
            dbc.Row([
                # Calculator section
                dbc.Col([
                    # Product name input
                    html.Div([
                        html.Label("Product Name", className="input-label"),
                        dbc.Input(id="product-name", type="text", className="input-box"),
                    ], className="input-group"),
                    
                    # Fraction display
                    html.Div([
                        html.Div([
                            html.Label("Nutritional Value (per 100g/100ml)", className="input-label"),
                            dbc.Input(id="numerator", type="number", className="input-box"),
                        ]),
                        html.Div(className="fraction-line"),
                        html.Div([
                            html.Label("Fixed Daily Requirement", className="input-label"),
                            dbc.Input(id="denominator", type="number", className="input-box"),
                        ]),
                        html.Div(" × 100 =", className="neon-text mt-2")
                    ], className="fraction"),
                    
                    # Result display
                    html.Div(id="result", className="text-center result-display neon-text"),
                    
                    # Buttons and signature row
                    html.Div([
                        # Left: Buttons
                        html.Div([
                            dbc.Button("Calculate", id="calculate-button", className="neon-button mx-2"),
                            dbc.Button("Clear Calculator", id="clear-calc-button", className="neon-button mx-2", color="warning")
                        ], className="d-flex align-items-center"),
                        # Right: Signature
                        html.Div("BUILT BY SXMXRTH 79", className="brand-signature")
                    ], className="d-flex justify-content-between align-items-center mb-3"),
                    
                
                ], width=8),
                
                # History section
                dbc.Col([
                    html.Div([
                        html.H4("History", className="neon-text history-title"),
                        html.Div(id="history-list"),
                        dbc.Button("Clear History", id="clear-history-button", className="neon-button mt-3 w-100")
                    ], className="history-section")
                ], width=4)
            ])
        ], className="main-container")
    ], fluid=True),
    
])

# Callback for calculation and history update
@app.callback(
    [Output("result", "children", allow_duplicate=True),
     Output("history-list", "children", allow_duplicate=True)],
    [Input("calculate-button", "n_clicks")],
    [State("product-name", "value"),
     State("numerator", "value"),
     State("denominator", "value"),
     State("history-list", "children")],
    prevent_initial_call=True
)
def update_output(n_clicks, product_name, numerator, denominator, history):
    if not n_clicks or not product_name or not numerator or not denominator:
        raise dash.exceptions.PreventUpdate
    
    try:
        rda_percentage = (float(numerator) / float(denominator)) * 100
        result = f"{rda_percentage:.1f}%"
        
        new_history_item = html.Div([
            html.Strong(f"{product_name}: "),
            html.Span(f"{numerator} / {denominator} = {result} RDA"),
            html.Div(f"({datetime.now().strftime('%H:%M:%S')})", 
                    style={"fontSize": "0.8em", "color": "#888"})
        ], className="history-item")
        
        history = history or []
        if isinstance(history, list):
            history.insert(0, new_history_item)
        else:
            history = [new_history_item]
        
        return result, history
    except Exception as e:
        return f"Error: {str(e)}", dash.no_update

# Callback for clearing calculator
@app.callback(
    [Output("product-name", "value", allow_duplicate=True),
     Output("numerator", "value", allow_duplicate=True),
     Output("denominator", "value", allow_duplicate=True),
     Output("result", "children", allow_duplicate=True)],
    Input("clear-calc-button", "n_clicks"),
    prevent_initial_call=True
)
def clear_calculator(n_clicks):
    if n_clicks:
        return "", None, None, ""
    raise dash.exceptions.PreventUpdate

# Callback for clearing history
@app.callback(
    Output("history-list", "children", allow_duplicate=True),
    Input("clear-history-button", "n_clicks"),
    prevent_initial_call=True
)
def clear_history(n_clicks):
    if n_clicks:
        return []
    raise dash.exceptions.PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True)