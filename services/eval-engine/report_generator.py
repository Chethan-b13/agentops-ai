from datetime import datetime
from pathlib import Path


class ReportGenerator:

    def generate(
        self,
        results: list[dict],
    ):
        report_dir = Path("../../reports")
        report_dir.mkdir(exist_ok=True)

        report = report_dir / "benchmark-report.md"

        passed = sum(r["passed"] for r in results)
        failed = len(results) - passed

        accuracy = (
            passed / len(results)
            if results
            else 0
        )

        lines = [
            "# 🚀 AgentOps AI Benchmark Report",
            "",
            f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}",
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|--------|------:|",
            f"| Benchmarks | {len(results)} |",
            f"| Passed | {passed} |",
            f"| Failed | {failed} |",
            f"| Accuracy | {accuracy:.0%} |",
            "",
            "---",
            "",
            "## Results",
            "",
            "| Benchmark | Score | Latency | Status |",
            "|-----------|-------|---------|--------|",
        ]

        for result in results:
            status = (
                "✅ PASS"
                if result["passed"]
                else "❌ FAIL"
            )

            latency = (
                f"{result['latency_ms']:.0f} ms"
                if result.get("latency_ms") is not None
                else "-"
            )

            lines.append(
                f"| {result['id']} | "
                f"{result['score']:.2f} | "
                f"{latency} | "
                f"{status} |"
            )

        report.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        return report