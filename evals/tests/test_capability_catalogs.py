from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[2]
EVALS = ROOT / "evals"


class CapabilityCatalogTests(unittest.TestCase):
    def _load(self, suite: str):
        path = EVALS / suite / "capabilities.json"
        self.assertTrue(path.is_file(), f"missing {suite} capability catalog")
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["suite"], suite)
        self.assertEqual(payload["arms"], ["icm", "cca", "no-skill"])
        return payload["capabilities"]

    def test_icm_parity_catalog_is_granular(self):
        capabilities = self._load("icm-parity")
        self.assertGreaterEqual(len(capabilities), 40)
        ids = [item["id"] for item in capabilities]
        self.assertEqual(len(ids), len(set(ids)))
        for item in capabilities:
            self.assertTrue(item["name"])
            self.assertTrue(item["must_test"])
        names = "\n".join(item["name"] for item in capabilities).lower()
        for anchor in ("setup", "status", "workspace-builder", "placeholder", "checkpoint", "audit", "factory/product", "progressive disclosure"):
            self.assertIn(anchor, names)

    def test_cca_extension_catalog_requires_discriminative_behavior(self):
        capabilities = self._load("cca-extensions")
        self.assertGreaterEqual(len(capabilities), 20)
        ids = [item["id"] for item in capabilities]
        self.assertEqual(len(ids), len(set(ids)))
        text = "\n".join(f"{item['name']} {item['must_test']}" for item in capabilities).lower()
        for anchor in ("zettelkasten", "llm wiki", "profile-aware", "nested authority", "method conflict", "non-trigger", "progressive-disclosure"):
            self.assertIn(anchor, text)


if __name__ == "__main__":
    unittest.main()
