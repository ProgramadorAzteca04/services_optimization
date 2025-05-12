import os

import pandas as pd


def export_report(report: list, filename: str = "report.xlsx"):
    df = pd.DataFrame(report)
    path = os.path.join("static", filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_excel(path, index=False)
    return filename
