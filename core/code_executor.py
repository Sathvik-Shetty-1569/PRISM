import io
import sys
from utils.security import validate_code
import pandas as pd
import matplotlib.pyplot as plt

def run_code(code, df):
    validate_code(code)
    output = io.StringIO()
    sys.stdout = output

    fig, ax = plt.subplots()

    safe_globals = {
        "df": df,
        "pd": pd,
        "plt": plt,
        "fig": fig,
        "ax": ax,
        "__builtins__": {
            "print": print,
            "len": len,
            "range": range,
            "min": min,
            "max": max,
            "sum": sum
        }
    }

    try:
        exec(code, safe_globals)
        text_result = output.getvalue()
        # Check if a plot was actually drawn
        has_plot = len(fig.axes) > 0 and any(
            len(ax.lines) + len(ax.collections) + 
            len(ax.patches) + len(ax.images) > 0 
            for ax in fig.axes
        )
    except Exception as e:
        sys.stdout = sys.__stdout__
        return str(e), None

    sys.stdout = sys.__stdout__
    return text_result, fig if has_plot else None