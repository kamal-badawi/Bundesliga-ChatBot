# Pandas Anzeigeoptionen anpassen
def get_pandas_Settings():
    import pandas as pd


    pd.set_option('display.max_columns', None)  # Zeige alle Spalten in DataFrame an
    pd.set_option('display.width', None)  # Keine Zeilenumbrüche
    pd.set_option('display.max_colwidth', None)  # Komplette Breite jeder DataFrame-Spalte
    pd.set_option('display.max_rows', 500)  # Zeige 500 Zeilen in DataFrame an
