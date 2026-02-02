# callbacks/__init__.py
from .counter_callbacks import register_counter_callbacks
from .map_callbacks import register_map_callbacks
from .plot_callbacks import register_plot_callbacks
from .table_callbacks import register_table_callbacks

def register_callbacks(app):
    register_counter_callbacks(app)
    register_map_callbacks(app)
    register_plot_callbacks(app)
    register_table_callbacks(app)
