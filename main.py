from dash import Dash, html, dcc, Input, Output, no_update, State
from dash_bootstrap_components.themes import BOOTSTRAP
from components.layout import create_layout
from components.callback import update_dataframe

def main():
    app = Dash(external_stylesheets=[BOOTSTRAP, '/assets/style.css'])
    app.title = "Inputs"
    app.layout = create_layout(app)

    # Assign the callback to the app object
    app.callback(
        Output('graph1','figure'),
        Output('graph2','figure'),  
        [
            Input('start_date', 'value'),
            Input('intervals_value', 'value'),
            Input('interval_value', 'value'),
            Input('demand_coef_slider','value'),
            Input('activity_coef_slider','value'),
            Input('initial_demand_value','value'),
            Input('initial_activity_value','value'),
            Input('wip_start_value','value'),
            Input('demand_growth_slider','value'),
            Input('activity_growth_slider','value'),
            Input('weekend_demand_label', 'value'),
            Input('sat_activity_label', 'value'),
            Input('sund_activity_label', 'value'),

            Input('check_update_1','value'),
            Input('update_date_value_1','value'),
            Input('update_demand_value_1','value'),
            Input('update_activity_value_1','value'),

            Input('check_update_2','value'),
            Input('update_date_value_2','value'),
            Input('update_demand_value_2','value'),
            Input('update_activity_value_2','value'),

            Input('check_update_3','value'),
            Input('update_date_value_3','value'),
            Input('update_demand_value_3','value'),
            Input('update_activity_value_3','value'),

            Input('check_update_4','value'),
            Input('update_date_value_4','value'),
            Input('update_demand_value_4','value'),
            Input('update_activity_value_4','value'),

            Input('check_update_5','value'),
            Input('update_date_value_5','value'),
            Input('update_demand_value_5','value'),
            Input('update_activity_value_5','value'),
            Input('Refresh', 'n_clicks')
        ],
    )(update_dataframe)

    app.run_server(debug=True)

if __name__ == "__main__":
    main()