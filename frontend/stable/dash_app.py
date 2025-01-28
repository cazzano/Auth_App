import dash
from dash import dcc, html, Input, Output, State
import requests

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div(
    className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-300 to-blue-500",
    children=[
        html.Div(
            className="bg-white shadow-lg rounded-lg p-8 w-96",
            children=[
                html.Div(
                    className="flex justify-center mb-4",
                    children=[
                        html.I(className='fas fa-user-circle text-6xl text-green-600')  # Logo as an icon
                    ]
                ),
                html.H1("Welcome Back!", className="text-2xl font-bold text-center mb-6 text-blue-600"),
                html.Div(
                    className="relative mb-4",
                    children=[
                        html.I(className="fas fa-user absolute left-3 top-3 text-gray-400"),  # User icon for username
                        dcc.Input(
                            id='username',
                            type='text',
                            placeholder='Username',
                            className='input input-bordered w-full pl-10 pr-3 py-2 rounded-md border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200',
                            style={'paddingLeft': '40px'},  # Increased padding to avoid overlap
                        ),
                    ]
                ),
                html.Div(
                    className="relative mb-6",
                    children=[
                        html.I(className="fas fa-lock absolute left-3 top-3 text-gray-400"),  # Key icon for password
                        dcc.Input(
                            id='password',
                            type='password',
                            placeholder='Password',
                            className='input input-bordered w-full pl-10 pr-3 py-2 rounded-md border-gray-300 focus:border-blue-500 focus:ring focus:ring-blue-200',
                            style={'paddingLeft': '40px'},  # Increased padding to avoid overlap
                        ),
                    ]
                ),
                html.Button(
                    [
                        html.I(className="fas fa-sign-in-alt mr-2"),  # Icon for the login button
                        "Login"
                    ],
                    id='login-button',
                    n_clicks=0,
                    className='btn btn-primary w-full bg-green-600 hover:bg-green-700 text-white rounded-md py-2 flex items-center justify-center'
                ),
                html.Div(id='output-message', className='mt-4 text-center text-red-600')
            ]
        )
    ]
)

# Callback to handle login
@app.callback(
    Output('output-message', 'children'),
    Input('login-button', 'n_clicks'),
    State('username', 'value'),
    State('password', 'value')
)
def login(n_clicks, username, password):
    if n_clicks > 0:
        if username and password:
            # Send a POST request to the Flask backend
            response = requests.post('http://127.0.0.1:5000/login', json={
                'username': username,
                'password': password
            })
            if response.status_code == 200:
                token = response.json().get('token')
                return f"Login successful! Token: {token}"
            else:
                return "Login failed! Please check your username and password."
        else:
            return "Please enter both username and password."
    return ""

# Include Tailwind CSS, DaisyUI, and Font Awesome CDN links
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Dash App</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/daisyui@1.14.0/dist/full.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    </head>
    <body>
        {%metas%}
        {%favicon%}
        {%css%}
        <div class="container mx-auto">
            {%app_entry%}
        </div>
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>
'''

if __name__ == '__main__':
    app.run_server(debug=True)
