from pathlib import Path

import yaml

from shared.evaluation import Benchmark


class BenchmarkLoader:

    def load(self, path: str | Path) -> Benchmark:
        path = Path(path)

        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return Benchmark.model_validate(data)