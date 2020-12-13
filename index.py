# -*- coding: utf-8 -*-
from app import app
import layouts
import callbacks

app.layout = layouts.serve_layout
app.title = 'I Energy'


if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_ui=False,
                   dev_tools_props_check=False, port=8059)

