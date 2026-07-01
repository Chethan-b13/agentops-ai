class Console:

    WIDTH = 70

    @staticmethod
    def divider():
        print("=" * Console.WIDTH)

    @staticmethod
    def header():

        print()
        Console.divider()
        print("🚀 AgentOps AI Evaluation Framework")
        Console.divider()

    @staticmethod
    def benchmark(benchmark):

        print()
        print(f"▶ {benchmark.id} - {benchmark.name}")

    @staticmethod
    def pass_result(score, latency):

        print(
            f"   ✅ PASS ({score:.0%})"
        )
        print(
            f"   ⏱ {latency:.0f} ms"
        )

    @staticmethod
    def fail_result(score, latency):

        print(
            f"   ❌ FAIL ({score:.0%})"
        )
        print(
            f"   ⏱ {latency:.0f} ms"
        )

    @staticmethod
    def summary(
        total,
        passed,
        markdown_report,
        json_report,
    ):
        Console.divider()

        failed = total - passed
        accuracy = passed / total if total else 0

        print(f"Total Benchmarks : {total}")
        print(f"Passed           : {passed}")
        print(f"Failed           : {failed}")
        print(f"Accuracy         : {accuracy:.0%}")

        print()

        print(f"Markdown Report  : {markdown_report}")
        print(f"JSON Report      : {json_report}")

        Console.divider()