import pandas as pd

def load_excel_data(file_path):
    """
    Loads an Excel file and returns a pandas DataFrame.

    Args:
        file_path: Path or file-like object of the uploaded Excel file.

    Returns:
        pd.DataFrame: Parsed Excel sheet.

    Raises:
        RuntimeError: If file cannot be read or is invalid.
    """
    try:
        df = pd.read_excel(file_path)
        if df.empty:
            raise ValueError("The uploaded Excel file is empty.")
        return df
    except Exception as e:
        raise RuntimeError(f"Error reading Excel file: {e}")
