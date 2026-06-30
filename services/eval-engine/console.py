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

        print(f"Total Benchmarks : {total}")
        print(f"Passed           : {passed}")
        print(f"Failed           : {total-passed}")
        print(f"Accuracy         : {passed/total:.0%}")

        print()

        print(f"Markdown Report  : {markdown_report}")
        print(f"JSON Report      : {json_report}")

        Console.divider()