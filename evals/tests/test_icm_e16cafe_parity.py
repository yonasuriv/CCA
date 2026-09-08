from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[2]
CCA = ROOT / "skills" / "cca"
ARCHITECT = CCA / "references" / "architect"
CORE = CCA / "references" / "core"
PARITY = ROOT / "evals" / "icm-parity" / "capabilities.json"


class ICME16CafeParityTests(unittest.TestCase):
    def test_restructure_requires_reference_integrity_before_approval(self):
        mode = (ARCHITECT / "mode.md").read_text(encoding="utf-8").lower()
        integrity_path = ARCHITECT / "reference-integrity.md"
        self.assertTrue(integrity_path.is_file(), "Architect must ship the restructure reference-integrity gate")
        integrity = integrity_path.read_text(encoding="utf-8").lower()
        combined = f"{mode}\n{integrity}"

        for anchor in (
            "referrer",
            "../",
            "symlink",
            "external",
            "case-fold",
            "copy",
            "verify",
            "remove",
        ):
            self.assertIn(anchor, combined, f"missing e16cafe restructure safety anchor: {anchor!r}")

        self.assertLess(
            mode.index("reference integrity"),
            mode.index("explicit approval"),
            "reference integrity must be checked before the restructure approval gate",
        )

    def test_system_map_walks_inbound_external_consumers(self):
        text = (ARCHITECT / "system-map.md").read_text(encoding="utf-8").lower()
        for anchor in ("inbound", "outside", "scheduled jobs", "agents"):
            self.assertIn(anchor, text, f"system map must cover reverse/inbound dependency discovery: {anchor!r}")

    def test_native_status_ignores_placeholder_only_outputs(self):
        text = (ARCHITECT / "native-icm-setup.md").read_text(encoding="utf-8").lower()
        self.assertIn("placeholder", text)
        self.assertIn("artifact", text)
        self.assertIn("status", text)

    def test_icm_inheritance_names_restructure_integrity_floor(self):
        text = (CORE / "icm-inheritance.md").read_text(encoding="utf-8").lower()
        for anchor in (
            "reference integrity",
            "case-fold",
            "copy-verify-remove",
            "inbound",
        ):
            self.assertIn(anchor, text, f"ICM inheritance map missing e16cafe capability: {anchor!r}")

    def test_parity_suite_tracks_e16cafe_capabilities(self):
        data = json.loads(PARITY.read_text(encoding="utf-8"))
        by_id = {capability["id"]: capability for capability in data["capabilities"]}
        expected = {
            "ICM-41": "Pre-move reference integrity",
            "ICM-42": "Case-fold destination collision",
            "ICM-43": "Copy-verify-remove migration",
            "ICM-44": "Inbound external consumers",
        }
        for capability_id, name in expected.items():
            self.assertIn(capability_id, by_id)
            self.assertEqual(name, by_id[capability_id]["name"])

        status = by_id["ICM-12"]["must_test"].lower()
        self.assertIn("placeholder", status)
        self.assertNotEqual(status, "derive complete/pending from real output folders, ignoring .gitkeep")


if __name__ == "__main__":
    unittest.main()
