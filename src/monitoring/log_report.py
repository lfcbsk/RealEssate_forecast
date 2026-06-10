import json
from datetime import datetime
from pathlib import Path


def save_monitoring_report(
    report: dict,
    output_dir="reports"
):

    Path(output_dir).mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = (
        datetime.now()
        .strftime("%Y%m%d_%H%M%S")
    )

    path = (
        Path(output_dir)
        / f"monitoring_{timestamp}.json"
    )

    with open(path, "w") as f:

        json.dump(
            report,
            f,
            indent=4,
            default=str
        )

    print(
        f"✓ Monitoring report saved -> {path}"
    )

    return path


def should_retrain(
    drift_ratio: float,
    performance_drop: float,
    drift_threshold: float = 0.3,
    performance_threshold: float = 0.2
):

    if drift_ratio > drift_threshold:
        return True

    if performance_drop > performance_threshold:
        return True

    return False