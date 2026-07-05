import importlib.util
import sqlite3
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT.parent / "fakedata.db"
GENERATOR_PATH = ROOT.parent / "fake_data_generator.py"
OLLAMA_PATH = ROOT.parent / "ollama_generator.py"


def _load_module(module_name: str, module_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fake_data_module = _load_module("fake_data_generator", GENERATOR_PATH)
ollama_module = _load_module("ollama_generator", OLLAMA_PATH)

FakeDataGenerator = fake_data_module.FakeDataGenerator
OllamaDataGenerator = ollama_module.OllamaDataGenerator
OllamaModelError = ollama_module.OllamaModelError


class DataService:
    def get_database_records(self) -> List[Dict[str, Any]]:
        if not DB_PATH.exists():
            raise FileNotFoundError("Database file not found")

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM fake_data").fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def generate_records(self, provider: str, count: int, model: str, base_url: str) -> Dict[str, Any]:
        if provider == "ollama":
            generator = OllamaDataGenerator(model=model, base_url=base_url)
            records = generator.generate_records(count=count)
        else:
            generator = FakeDataGenerator()
            records = generator.generate_users(count=count)

        return {"provider": provider, "count": count, "records": records}
