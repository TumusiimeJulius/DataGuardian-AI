import csv
import os

try:
    import pandas as pd
except ImportError:  # pragma: no cover - exercised in minimal environments
    pd = None


CLEAN_FOLDER = "cleaned"


os.makedirs(
    CLEAN_FOLDER,
    exist_ok=True
)



def repair_dataset(file_path):
    if pd is not None:
        df = pd.read_csv(file_path)

        original_rows = len(df)

        # Remove duplicate rows
        duplicates = df.duplicated().sum()
        df = df.drop_duplicates()

        # Fill missing values
        for column in df.columns:
            if df[column].dtype == "object":
                df[column] = df[column].fillna("Unknown")
            else:
                df[column] = df[column].fillna(df[column].median())

        cleaned_rows = len(df)

        filename = os.path.basename(file_path)
        clean_filename = filename.replace(".csv", "_cleaned.csv")
        output_path = os.path.join(CLEAN_FOLDER, clean_filename)

        df.to_csv(output_path, index=False)

        return {
            "clean_file": clean_filename,
            "removed_duplicates": int(duplicates),
            "original_rows": original_rows,
            "cleaned_rows": cleaned_rows,
            "path": output_path,
        }

    if not file_path.lower().endswith(".csv"):
        return {"error": "pandas is unavailable and Excel repair requires pandas"}

    with open(file_path, "r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    original_rows = len(rows)
    seen = set()
    cleaned_rows = []
    duplicates = 0

    for row in rows:
        row_tuple = tuple(row.get(key, "") for key in row.keys())
        if row_tuple in seen:
            duplicates += 1
            continue
        seen.add(row_tuple)
        cleaned_rows.append({
            key: (value if value not in {"", None} else "Unknown")
            for key, value in row.items()
        })

    filename = os.path.basename(file_path)
    clean_filename = filename.replace(".csv", "_cleaned.csv")
    output_path = os.path.join(CLEAN_FOLDER, clean_filename)

    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(cleaned_rows[0].keys()) if cleaned_rows else [])
        if cleaned_rows:
            writer.writeheader()
            writer.writerows(cleaned_rows)

    return {
        "clean_file": clean_filename,
        "removed_duplicates": int(duplicates),
        "original_rows": original_rows,
        "cleaned_rows": len(cleaned_rows),
        "path": output_path,
    }