import json
from datetime import datetime
from pathlib import Path


class JsonReportGenerator:

    def generate(self, results: list[dict]):

        report_dir = Path("../../reports")
        report_dir.mkdir(exist_ok=True)

        report_path = report_dir / "benchmark-results.json"

        passed = sum(
            r["passed"] for r in results
        )

        accuracy = (
            passed / len(results)
            if results
            else 0
        )

        report = {
            "generated_at": str(datetime.now()),
            "summary": {
                "benchmarks": len(results),
                "passed": passed,
                "failed": len(results) - passed,
                "accuracy": accuracy,
            },
            "results": results,
        }

        report_path.write_text(
            json.dumps(report, indent=2),
            encoding="utf-8",
        )

        return report_path