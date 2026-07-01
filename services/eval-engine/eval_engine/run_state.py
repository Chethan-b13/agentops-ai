import json
from pathlib import Path


class RunState:

    def __init__(self):
        self.state_file = Path("../../reports/run-state.json")

        self.state_file.parent.mkdir(
            exist_ok=True
        )

    def load(self):

        if not self.state_file.exists():
            return {
                "completed": [],
                "results": [],
            }

        return json.loads(
            self.state_file.read_text()
        )

    def save(
        self,
        completed,
        results,
    ):

        self.state_file.write_text(
            json.dumps(
                {
                    "completed": completed,
                    "results": results,
                },
                indent=2,
            )
        )

    def reset(self):

        if self.state_file.exists():
            self.state_file.unlink()