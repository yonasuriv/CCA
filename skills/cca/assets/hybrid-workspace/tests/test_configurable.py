"""Configurable profile regression coverage."""
import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from configurable import compose
from schema import generated_outputs


class ConfigurableTests(unittest.TestCase):
    def test_owner_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = {"schema_version": 5, "cca": {"specification": "1.6.0"},
                   "bindings": {"wiki": {"role": "knowledge.durable", "path": "wiki/"},
                                "tools": {"role": "system.operations", "path": "tools/"}},
                   "generation": {"outputs": {"setup": {"renderer": "mkdirs", "slot": "tools", "file": "setup.py"}}}}
            self.assertEqual(generated_outputs(compose(raw, root, "workspace.yaml")), {"setup": "tools/setup.py"})
            raw["bindings"]["renamed"] = raw["bindings"].pop("wiki")
            raw["bindings"]["tools"]["path"] = "ops/"
            self.assertEqual(generated_outputs(compose(raw, root, "workspace.yaml")), {"setup": "ops/setup.py"})
            del raw["bindings"]["renamed"]
            compose(raw, root, "workspace.yaml")
            del raw["bindings"]["tools"]
            with self.assertRaises(ValueError):
                compose(raw, root, "workspace.yaml")
            raw["generation"]["outputs"].clear()
            compose(raw, root, "workspace.yaml")
