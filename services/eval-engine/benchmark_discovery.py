from pathlib import Path


class BenchmarkDiscovery:

    def discover(self, root: str | Path):

        root = Path(root)

        return sorted(
            root.rglob("*.yaml")
        )