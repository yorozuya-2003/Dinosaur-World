# import dash
# from dash import html
# from dash.dependencies import Input, Output, State
# from style import styles

# external_stylesheets = ['https://unpkg.com/boxicons@2.0.7/css/boxicons.min.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# html_UL_css = styles[".sidebar .nav-links li .sub-menu"]

# sidebar = html.Div([
#     html.Div([
#         html.I(className='bx bxl-c-plus-plus', style=styles[".sidebar .logo-details i"]),
#         html.Span('CodingLab', className='logo_name', style=styles[".sidebar .logo-details .logo_name"]),
#     ], className='logo-details', style=styles[".sidebar .logo-details"]),
#     html.Ul([
#         html.Li([
#             html.A([
#                 html.I(className='bx bx-grid-alt', style=styles[".sidebar .nav-links li i"]),
#                 html.Span('Dashboard', className='link_name', style=styles[".sidebar .nav-links li a .link_name"]),
#             ], style=styles[".sidebar .nav-links li a"]),
#             html.Ul(className='sub-menu blank', style=styles[".sidebar .nav-links li .sub-menu.blank"]),
#         ], style=styles[".sidebar .nav-links li"]),
#         html.Li([
#             html.Div([
#                 html.A([
#                     html.I(className='bx bx-collection', style=styles[".sidebar .nav-links li i"]),
#                     html.Span('Category', className='link_name', style=styles[".sidebar .nav-links li a .link_name"]),
#                 ], style=styles[".sidebar .nav-links li a"]),
#                 html.I(className='bx bxs-chevron-down arrow', style=styles[".sidebar .nav-links li i"], id='arrow'),
#             ], className='iocn-link', style=styles[".sidebar .nav-links li .iocn-link"]),
#             # html.Ul([
#             #     html.Li([html.A('Category', className='link_name', href='#', style=styles[".sidebar .nav-links li .sub-menu a"])]),
#             #     html.Li([html.A('HTML & CSS', href='#', style=styles[".sidebar .nav-links li .sub-menu a"])]),
#             #     html.Li([html.A('JavaScript', href='#', style=styles[".sidebar .nav-links li .sub-menu a"])]),
#             #     html.Li([html.A('PHP & MySQL', href='#', style=styles[".sidebar .nav-links li .sub-menu a"])]),
#             # ], className='sub-menu', style=styles[".sidebar .nav-links li .sub-menu"], id='sub-menu-bar'),
#             # html.Ul(className='sub-menu', style=styles[".sidebar .nav-links li .sub-menu"], id='sub-menu'),
#             html.Ul(id='sub-menu'),
#         ], style=styles[".sidebar .nav-links li"]),
#         # Add more menu items here
#     ], className='nav-links', style=styles[".sidebar .nav-links"]),
# ], className='sidebar close', style=styles[".sidebar"], id='sidebar')

# app.layout = html.Div([
#     html.Div([
#         sidebar,
#         html.Section([
#             html.Div([
#                 html.I(className='bx bx-menu', id='menu-btn', style=styles[".home-section .home-content .bx-menu"]),
#                 html.Span('Drop Down Sidebar', className='text', style=styles[".home-section .home-content .text"]),
#             ], className='home-content', style=styles[".home-content"]),
#         ], className='home-section', style=styles[".home-section"]),
#     ], style={'display': 'flex'})
# ])

# in_style = styles[".sidebar .nav-links li .sub-menu a"]
# # html_UL_css = styles[".sidebar .nav-links li .sub-menu"]

# @app.callback(
#     Output('sub-menu', 'children'),
#     Input('arrow', 'n_clicks'),
#     State('sub-menu', 'className')
# )

# def toggle_submenu(n_clicks, submenu_class):
#     print(n_clicks)
#     ul_style = {
#         "color": "#fff",
#         "font-size": "15px",
#         "padding": "5px 0",
#         "white-space": "nowrap",
#         "opacity": "0.6",
#         "transition": "all 0.3s ease",
#     }

#     ul_style_2 = {
#         "padding": "6px 6px 14px 80px",
#         "margin-top": "-10px",
#         "background": "#000",
#         "display": "none",
#     }

#     if n_clicks and n_clicks % 2 == 1:
#         print(0)
#         # return html.Ul([
#         #         html.Li([html.A('Category', className='link_name', href='#', style=styles[".sidebar .nav-links li .sub-menu a"])]),
#         #         html.Li([html.A('HTML & CSS', href='#', style=styles[".sidebar .nav-links li .sub-menu a"])]),
#         #         html.Li([html.A('JavaScript', href='#', style=styles[".sidebar .nav-links li .sub-menu a"])]),
#         #         html.Li([html.A('PHP & MySQL', href='#', style=styles[".sidebar .nav-links li .sub-menu a"])]),
#         #     ]),
#         # return 'sub-menu-bar' if 'blank' in submenu_class else 'sub-menu blank'
#         # return 'sub-menu-bar'
#         return html.Ul([
#             html.Li([html.A('HTML & CSS', href='#', style=ul_style)]),
#             html.Li([html.A('JavaScript', href='#', style=ul_style)]),
#             html.Li([html.A('PHP & MySQL', href='#', style=ul_style)]),
#         ])
#     else:
#         # return submenu_class
#         return html.Ul(style=ul_style_2)

# if __name__ == '__main__':
#     app.run_server(debug=True)
import requests
from bs4 import BeautifulSoup

# Send a GET request to the webpage
url = "https://www.nhm.ac.uk/discover/dino-directory/aardonyx.html"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup)
    # Find the element containing the image source
    image_container = soup.find('div', class_='dinosaur--comparison-dino')  # Adjust class name as needed
    
    # Extract the source attribute from the img tag within the container
    if image_container:
        image_element = image_container.find('img')
        if image_element:
            image_src = image_element.get('src')
            print("Image source:", image_src)
        else:
            print("Image not found within the container.")
    else:
        print("Image container not found on the page.")
else:
    print("Failed to fetch webpage.")

