import sys
import os
import pandas as pd
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from checker import calculate_strength

def load_passwords(filepath: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(filepath)
        if "password" not in df.columns:
            raise ValueError("CSV must have a 'password' column.")
        df = df.dropna(subset=["password"])
        df["password"] = df["password"].astype(str)
        print(f"  Loaded {len(df)} passwords from '{filepath}'")
        return df
    except FileNotFoundError:
        print(f"  File not found: {filepath}")
        sys.exit(1)


def run_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply strength checker to every row.
    Extracts nested result fields into flat columns.
    """
    results = df["password"].apply(calculate_strength)

    df["strength"]     = results.apply(lambda r: r["strength"])
    df["score"]        = results.apply(lambda r: r["score"])
    df["length"]       = results.apply(lambda r: r["details"]["length"]["length"])
    df["has_upper"]    = results.apply(lambda r: r["details"]["variety"]["uppercase"])
    df["has_lower"]    = results.apply(lambda r: r["details"]["variety"]["lowercase"])
    df["has_digit"]    = results.apply(lambda r: r["details"]["variety"]["digit"])
    df["has_symbol"]   = results.apply(lambda r: r["details"]["variety"]["symbol"])
    df["is_common"]    = results.apply(lambda r: r["details"]["is_common"])
    df["has_repeats"]  = results.apply(lambda r: r["details"]["has_repeats"])
    df["feedback"]     = results.apply(lambda r: " | ".join(r["feedback"]))
    df["password_masked"] = df["password"].apply(lambda p: p[0] + "*" * (len(p)-2) + p[-1] if len(p) > 2 else "**")

    return df


def print_summary(df: pd.DataFrame):
    total = len(df)
    counts = df["strength"].value_counts()

    print("\n" + "=" * 50)
    print("  📊  BATCH ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"  Total passwords analyzed  : {total}")
    print(f"  STRONG passwords          : {counts.get('STRONG', 0)} ({counts.get('STRONG', 0)/total*100:.1f}%)")
    print(f"  MEDIUM passwords          : {counts.get('MEDIUM', 0)} ({counts.get('MEDIUM', 0)/total*100:.1f}%)")
    print(f"  WEAK passwords            : {counts.get('WEAK',   0)} ({counts.get('WEAK',   0)/total*100:.1f}%)")
    print("—" * 50)
    print(f"  Average score             : {df['score'].mean():.2f} / 7")
    print(f"  Average length            : {df['length'].mean():.1f} characters")
    print(f"  Common/leaked passwords   : {df['is_common'].sum()}")
    print(f"  With repeated chars       : {df['has_repeats'].sum()}")
    print("—" * 50)
    print(f"\n  Character Variety (% of total passwords):")
    print(f"    Has uppercase  : {df['has_upper'].mean()*100:.1f}%")
    print(f"    Has lowercase  : {df['has_lower'].mean()*100:.1f}%")
    print(f"    Has digits     : {df['has_digit'].mean()*100:.1f}%")
    print(f"    Has symbols    : {df['has_symbol'].mean()*100:.1f}%")
    print("=" * 50 + "\n")


def save_report(df: pd.DataFrame, output_dir: str = "../reports"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_cols = [
        "password_masked", "strength", "score", "length",
        "has_upper", "has_lower", "has_digit", "has_symbol",
        "is_common", "has_repeats", "feedback"
    ]
    detail_path = os.path.join(output_dir, f"analysis_detail_{timestamp}.csv")
    df[output_cols].to_csv(detail_path, index=False)
    print(f"  Detailed report saved → {detail_path}")
    summary_data = {
        "metric": [
            "total", "strong", "medium", "weak",
            "avg_score", "avg_length", "common_count", "repeat_count"
        ],
        "value": [
            len(df),
            int((df["strength"] == "STRONG").sum()),
            int((df["strength"] == "MEDIUM").sum()),
            int((df["strength"] == "WEAK").sum()),
            round(df["score"].mean(), 2),
            round(df["length"].mean(), 2),
            int(df["is_common"].sum()),
            int(df["has_repeats"].sum())
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_path = os.path.join(output_dir, f"analysis_summary_{timestamp}.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"  Summary report saved     → {summary_path}")


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else "../data/sample_passwords.csv"

    print("\n  🔍  DecodeLabs — Password Batch Analyzer")
    print("  " + "—" * 40)

    df = load_passwords(input_file)
    df = run_analysis(df)
    print_summary(df)
    save_report(df)


if __name__ == "__main__":
    main()
