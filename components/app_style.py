import os
import base64




nav_bar_color = "#05322B"
page_background_color = '#F8FAF9'
text_color = nav_bar_color
text_color1 = "#147D64"
card_col = '#FFFFFF',
card_col1 = '#F8FAF9',
odd_row_col = '#C6F7E2'
even_row_col = '#EFFCF6'
tab_border_col = '#05322B'
tab_background = "#EBEFEE"
highlight = "#02BC94"
tab_border_color = '#CED7D4'
table_header_bod_col = '#8CA39D'
table_header_col = '#CED7D4'
even_row_col1 = '#F8FAF9'
implemented_col = '#02A783'
ongoing_col = "#FADB5F"
to_be_started_col = "#E12D39"
header_text_color = nav_bar_color


act_table_cols = ['Event date', 'Event type', 'Project', 'EBS', 'System', 'Group', 'Component', 'Status']
top_offenders = ["Failed start", 'Trip', 'Maintenance']




font_family = 'Areal'



# Images
logo_file = os.path.join(os.getcwd(), "input/static", 'logo.png')
next_icon = os.path.join(os.getcwd(), "input/static", 'next.png')
previous_icon = os.path.join(os.getcwd(), "input/static", 'previous.png')
previous_icon_disabled = os.path.join(os.getcwd(), "input/static", 'prev_disabled.png')
next_icon_disabled = os.path.join(os.getcwd(), "input/static", 'next_disabled.png')
default_img_file = os.path.join(os.getcwd(), "static", 'default.png')


def get_color():
    while True:
        for color in colors:
            yield color


def encode_image(img_file):
    encoded_image = base64.b64encode(open(img_file, 'rb').read())
    return f'data:image/png;base64,{encoded_image.decode()}'



# Styles

field_height_global = "45px"

tabs_styles = {
    'height': '40px',
    'marginTop': 5
}
tab_style = {
    'borderTop': f'1px solid {nav_bar_color}',
    'borderBottom': f'1px solid {nav_bar_color}',
    'borderLeft': f'1px solid {nav_bar_color}',
    'borderRight': f'1px solid {nav_bar_color}',
    'padding': '2px',
    "font-size": "24px",
    "font-family": font_family,
    'backgroundColor': nav_bar_color,
    'color': card_col,
    # "border-radius": "5px"
}


tab_selected_style = {
    'borderTop': f'1px solid {nav_bar_color}',
    'borderBottom': f'1px solid {nav_bar_color}',
    'borderLeft': f'1px solid {nav_bar_color}',
    'borderRight': f'1px solid {nav_bar_color}',
    'fontWeight': 'bold',
    'backgroundColor': nav_bar_color,  # Green
    'color': card_col,
    'padding': '2px',
    "font-size": "24px",
    "font-family": font_family,
    # "border-radius": "5px"
}

page_style = {'backgroundColor': page_background_color,
              'marginLeft': 30,
              'marginRight': 30}

layout_style = {'backgroundColor': page_background_color,
                "font-family": font_family}



legend_style = {'x': 0.02, 'y': 1.1,
                'font': {'size': 12,
                         'family': font_family},
                'orientation': 'h'}

legend_style2 = {'x': 0.02, 'y': 1.2,
                 'font': {'size': 12,
                          'family': font_family},
                 'orientation': 'h'}

legend_style4 = {'x': 0, 'y': 1.3,
                 'font': {'size': 12,
                          'family': font_family},
                 'orientation': 'h'}


checklist_style1 = {"font-size": "14px",
              "font-family": font_family,
              "color": text_color,
                'float': 'bottom',
                "zoom": 1.5
                }

checklist_label_style1 = {'display': 'inline-block',
                                'cursor': 'pointer',
                                'margin-right': '20px',
                   'float': 'top'
                   }


radio_style1 = {"font-size": "14px",
              "font-family": font_family,
              "color": text_color,
                'float': 'bottom'
                }

radio_label_style1 = {
                    'cursor': 'pointer',
                    'margin-right': '20px',
                   'float': 'top'
                   }

radio_input_style1 = {'float': 'bottom', 'margin-right': '5px',
                      }
label_style1 = {"font-size": "20px",
              "font-family": font_family,
              'fontWeight': 'bold',
              "color": text_color,
                'float': 'bottom'}

label_style2 = {"font-size": "18px",
              "font-family": font_family,
              "color": text_color,
              'fontWeight': 'bold',
                'float': 'top'
                }

label_style3 = {"font-size": "14px",
              "font-family": font_family,
              "color": text_color,
                'float': 'top'
                }

label_style4 = {"font-size": "18px",
              "font-family": font_family,
              "color": highlight,
              'fontWeight': 'bold',
                'float': 'center'
                }


dropdown_style = {"font-size": "15px",
                  "font-family": font_family,
                  "color": "#02BC94",
                  'marginBottom': 10,
                  }

graph_style1 = {'height': '450px'}

button_div_style = {'display': 'inline-block', "width": '33.33%'}
button_style1 = {"height": "200px", 'width': '93%', "font-family": font_family,
                 "font-size": "14px", 'border': f'1px solid {nav_bar_color}',
                 'borderTop': f'5px solid {nav_bar_color}'}

lbl_text_style = {"height": "30px",
                  "font-size": "18px"}

legend_style1 = {'x': 0.02, 'y': 1,
                 'font': {'size': 12,
                          'family': font_family},
                 'orientation': 'h'}

next_icon_height = '30px'
info_icon_height = '20px'
next_icon_style = {'color': nav_bar_color,
                   'backgroundColor': card_col,
                   'height': '40px',
                   # "font-size": "15px",
                   'width': '40px',
                   # 'float': 'top',
                   "border": f"1px {card_col}",
                   'border-style': 'hidden'}
