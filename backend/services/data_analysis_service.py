import csv
import os

try:
    import pandas as pd
except ImportError:  # pragma: no cover - exercised in minimal environments
    pd = None


def analyze_dataset(file_path):
    try:
        if pd is not None:
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
                df = pd.read_excel(file_path)
            else:
                return {"error": "Unsupported file format"}

            rows = len(df)
            columns = len(df.columns)
            missing_values = int(df.isnull().sum().sum())
            duplicates = int(df.duplicated().sum())

            total_cells = rows * columns
            if total_cells > 0:
                quality_score = round((1 - (missing_values + duplicates) / total_cells) * 100, 2)
            else:
                quality_score = 0

            anomalies = 0
            numeric_columns = df.select_dtypes(include="number")
            for column in numeric_columns:
                mean = numeric_columns[column].mean()
                std = numeric_columns[column].std()
                if std != 0:
                    outliers = df[abs(df[column] - mean) > 3 * std]
                    anomalies += len(outliers)

            recommendations = []
            if missing_values > 0:
                recommendations.append("Fill missing values using appropriate methods")
            if duplicates > 0:
                recommendations.append("Remove duplicate records")
            if anomalies > 0:
                recommendations.append("Investigate detected abnormal records")
            if quality_score > 90:
                recommendations.append("Dataset quality is excellent")

            return {
                "dataset": os.path.basename(file_path),
                "rows": rows,
                "columns": columns,
                "missing_values": missing_values,
                "duplicates": duplicates,
                "anomalies": anomalies,
                "quality_score": quality_score,
                "recommendations": recommendations,
            }

        if not file_path.lower().endswith(".csv"):
            return {"error": "pandas is unavailable and Excel analysis requires pandas"}

        with open(file_path, "r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)

        columns = len(rows[0].keys()) if rows else 0
        row_count = len(rows)
        missing_values = sum(1 for row in rows for value in row.values() if value in {"", None})
        seen = set()
        duplicates = 0
        for row in rows:
            row_tuple = tuple(row.get(key, "") for key in row.keys())
            if row_tuple in seen:
                duplicates += 1
            else:
                seen.add(row_tuple)

        total_cells = row_count * columns
        if total_cells > 0:
            quality_score = round((1 - (missing_values + duplicates) / total_cells) * 100, 2)
        else:
            quality_score = 0

        recommendations = []
        if missing_values > 0:
            recommendations.append("Fill missing values using appropriate methods")
        if duplicates > 0:
            recommendations.append("Remove duplicate records")
        if quality_score > 90:
            recommendations.append("Dataset quality is excellent")

        return {
            "dataset": os.path.basename(file_path),
            "rows": row_count,
            "columns": columns,
            "missing_values": missing_values,
            "duplicates": duplicates,
            "anomalies": 0,
            "quality_score": quality_score,
            "recommendations": recommendations,
        }

    except Exception as e:
        return {"error": str(e)}