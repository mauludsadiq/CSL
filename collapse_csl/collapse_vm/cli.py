import argparse
import json
import pandas as pd
from collapse_vm.interpreter import execute_script

def load_config_from_csv(csv_path):
    try:
        df = pd.read_csv(csv_path)
        config = {}
        for _, row in df.iterrows():
            key = str(row.get("key")).strip().lower()
            value = row.get("value")
            if key in {"mutate", "target"}:
                config[key] = int(value) if key == "target" else float(value)
            elif key in {"report"}:
                config[key] = str(value).lower() == "true"
            elif key in {"theme", "curve", "format"}:
                config[key] = str(value).strip().lower()
        return config
    except Exception as e:
        raise RuntimeError(f"Failed to parse CSV config: {e}")

def run():
    parser = argparse.ArgumentParser(description="Collapse Symbolic Language (CSL) Interpreter")

    parser.add_argument("filename", help="Input CSL script file")
    parser.add_argument("--mutate", type=float, help="Mutation probability (0.0–1.0)")
    parser.add_argument("--curve", type=str, choices=["linear", "sigmoid", "inverse"],
                        help="Mutation curve type")
    parser.add_argument("--report", action="store_true", help="Generate trace report and visualization")
    parser.add_argument("--theme", type=str, help="Visualization theme (e.g., ggplot)")
    parser.add_argument("--target", type=int, help="Target collapse index (for analysis)")
    parser.add_argument("--format", type=str, choices=["gif", "mp4"], help="Output format")
    parser.add_argument("--csv", type=str, help="Path to CSV file with config (key,value columns)")

    args = parser.parse_args()

    # Load and override defaults from CSV
    config = {
        "mutate_prob": args.mutate,
        "curve": args.curve,
        "report": args.report,
        "theme": args.theme,
        "target": args.target,
        "output_format": args.format
    }

    if args.csv:
        csv_config = load_config_from_csv(args.csv)
        config.update({  # Only override if values in CSV are not None
            "mutate_prob": csv_config.get("mutate", config["mutate_prob"]),
            "curve": csv_config.get("curve", config["curve"]),
            "report": csv_config.get("report", config["report"]),
            "theme": csv_config.get("theme", config["theme"]),
            "target": csv_config.get("target", config["target"]),
            "output_format": csv_config.get("format", config["output_format"])
        })

    # Apply defaults if still unset
    config["mutate_prob"] = config["mutate_prob"] if config["mutate_prob"] is not None else 0.0
    config["curve"] = config["curve"] if config["curve"] else "linear"
    config["theme"] = config["theme"] if config["theme"] else "default"
    config["output_format"] = config["output_format"] if config["output_format"] else "gif"

    execute_script(
        filename=args.filename,
        mutate_prob=config["mutate_prob"],
        curve=config["curve"],
        report=config["report"],
        theme=config["theme"],
        target=config["target"],
        output_format=config["output_format"]
    )
