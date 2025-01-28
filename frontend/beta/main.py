import dash
from dash import dcc, html, Input, Output, State
import requests
import json

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Authentication App"),
    dcc.Input(id='username', type='text', placeholder='Enter Username'),
    dcc.Input(id='password', type='password', placeholder='Enter Password'),
    html.Button('Login', id='login-button', n_clicks=0),
    html.Div(id='login-message', style={'margin-top': '20px'}),
    html.Div(id='protected-content', style={'margin-top': '20px'}),
    dcc.Store(id='token-store')  # Store the JWT token
])

# Combined callback for login and accessing protected content
@app.callback(
    Output('login-message', 'children'),
    Output('protected-content', 'children'),
    Output('token-store', 'data'),
    Input('login-button', 'n_clicks'),
    State('username', 'value'),
    State('password', 'value'),
    State('token-store', 'data'),
)
def handle_login(n_clicks, username, password, token):
    if n_clicks > 0:
        if username and password:
            # Make a POST request to the login endpoint
            response = requests.post('http://127.0.0.1:5000/login', json={
                'username': username,
                'password': password
            })
            if response.status_code == 200:
                token = response.json().get('token')
                # Now access the protected content
                headers = {'x-access-token': token}
                protected_response = requests.get('http://127.0.0.1:5000/protected', headers=headers)
                if protected_response.status_code == 200:
                    protected_message = protected_response.json().get('message')
                    return "Login successful!", protected_message, token
                else:
                    return "Login successful!", "Access denied! Token may be invalid.", token
            else:
                return "Login failed! Check your username and password.", "", None
    return "", "", None

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
