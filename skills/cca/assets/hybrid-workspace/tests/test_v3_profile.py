#!/usr/bin/env python3
# Regression tests for the opt-in Hybrid Workspace schema v3 and its v2 compatibility.
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

PACKAGE = Path(__file__).resolve().parents[1]
V2 = PACKAGE / "profiles" / "v2"
sys.path.insert(0, str(PACKAGE))
import provenance  # noqa: E402
import schema as schema_module  # noqa: E402


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(args), cwd=cwd or PACKAGE, text=True, capture_output=True, check=False)


def audit(target: Path) -> subprocess.CompletedProcess[str]:
    return run(sys.executable, str(PACKAGE / "audit.py"), "--target", str(target))


def generate(target: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return run(sys.executable, str(PACKAGE / "generate.py"), "--target", str(target), *extra)


def make_target(source: Path = PACKAGE) -> Path:
    target = Path(tempfile.mkdtemp(prefix="cca-hybrid-v3-"))
    for name in ("WORKSPACE.yaml", "AGENTS.md"):
        shutil.copy2(source / name, target / name)
    return target


def load(target: Path) -> dict:
    return yaml.safe_load((target / "WORKSPACE.yaml").read_text(encoding="utf-8"))


def save(target: Path, data: dict) -> None:
    (target / "WORKSPACE.yaml").write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def set_binding(target: Path, key: str, binding: str) -> None:
    data = load(target)
    next(s for s in data["slots"] if s["key"] == key)["binding"] = binding
    save(target, data)


def body_hash(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def clip(body: str = "Article body.\n", **overrides: str) -> str:
    prov = {
        "origin": "https://example.com/article",
        "acquired_by": "human:owner",
        "acquisition_method": "obsidian-web-clipper",
        "acquired_at": "2026-10-30T12:00:00+01:00",
        "content_hash": body_hash(body),
        "content_hash_scope": "body",
    }
    prov.update(overrides)
    front = yaml.safe_dump({"title": "Article", "tags": ["clippings"], "provenance": prov}, sort_keys=False)
    return f"---\n{front}---\n{body}"


def failures(result: subprocess.CompletedProcess[str]) -> str:
    return result.stdout + result.stderr


class V3TemplateAndGenerationTests(unittest.TestCase):
    def test_bundled_template_is_v3_and_passes_audit_and_check(self) -> None:
        target = make_target()
        self.assertEqual(load(target)["schema_version"], 3)
        self.assertEqual(generate(target).returncode, 0)
        result = generate(target, "--check")
        self.assertEqual(result.returncode, 0, failures(result))

    def test_workspace_yaml_is_the_only_generated_root_dependency(self) -> None:
        target = make_target()
        self.assertEqual(generate(target).returncode, 0)
        root_files = sorted(p.name for p in target.iterdir() if p.is_file())
        # Only the bootstrap anchor, the human control file and the router binding remain at root.
        self.assertEqual(root_files, ["AGENTS.md", "CONTEXT.md", "WORKSPACE.yaml"])
        for name in ("paths.sh", "mkdirs.sh", "obsidian-excludes.txt", "SPEC.md"):
            self.assertFalse((target / name).exists(), name)
        self.assertTrue((target / "_runtime/operations/paths.sh").is_file())
        self.assertTrue((target / "_runtime/docs/SPEC.md").is_file())

    def test_generated_outputs_follow_their_slot_bindings(self) -> None:
        target = make_target()
        set_binding(target, "system.operations", "ops/generated/")
        set_binding(target, "system.documentation", "handbook/")
        set_binding(target, "context.router", "ROUTER.md")
        self.assertEqual(generate(target).returncode, 0)
        for rel in ("ops/generated/paths.sh", "ops/generated/mkdirs.sh", "ops/generated/obsidian-excludes.txt", "handbook/SPEC.md", "ROUTER.md"):
            self.assertTrue((target / rel).is_file(), rel)
        self.assertFalse((target / "_runtime").exists())
        self.assertEqual(generate(target, "--check").returncode, 0)
        spec = (target / "handbook/SPEC.md").read_text(encoding="utf-8")
        self.assertIn("ops/generated/paths.sh", spec)
        self.assertNotIn("_runtime/operations", spec)

    def test_helpers_resolve_actual_root_not_their_own_directory(self) -> None:
        target = make_target()
        set_binding(target, "system.operations", "a/b/c/")
        self.assertEqual(generate(target).returncode, 0)
        outside = Path(tempfile.mkdtemp(prefix="cca-cwd-"))
        sourced = run("bash", "-c", f'source "{target}/a/b/c/paths.sh" && echo "$WS_ROOT|${{WS[knowledge.durable]}}"', cwd=outside)
        self.assertEqual(sourced.returncode, 0, failures(sourced))
        root, durable = sourced.stdout.strip().split("|")
        self.assertEqual(Path(root), target.resolve())
        self.assertEqual(Path(durable), target.resolve() / "00-wiki")
        made = run("bash", str(target / "a/b/c/mkdirs.sh"), "--required", cwd=outside)
        self.assertEqual(made.returncode, 0, failures(made))
        self.assertTrue((target / "00-wiki").is_dir())
        self.assertFalse((target / "a/b/c/00-wiki").exists())
        self.assertFalse((outside / "00-wiki").exists())

    def test_zsh_can_source_relocated_paths(self) -> None:
        if shutil.which("zsh") is None:
            self.skipTest("zsh not installed")
        target = make_target()
        self.assertEqual(generate(target).returncode, 0)
        result = run("zsh", "-c", f'source "{target}/_runtime/operations/paths.sh" && print -r -- "$WS_ROOT"')
        self.assertEqual(result.returncode, 0, failures(result))
        self.assertEqual(Path(result.stdout.strip()), target.resolve())

    def test_copied_helper_fails_closed_instead_of_guessing_a_root(self) -> None:
        target = make_target()
        self.assertEqual(generate(target).returncode, 0)
        stray = Path(tempfile.mkdtemp(prefix="cca-stray-")) / "x" / "y"
        stray.mkdir(parents=True)
        shutil.copy2(target / "_runtime/operations/mkdirs.sh", stray / "mkdirs.sh")
        result = run("bash", str(stray / "mkdirs.sh"), "--all")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workspace root not found", result.stderr)
        self.assertFalse((stray / "00-wiki").exists())
        self.assertFalse((stray.parent.parent / "00-wiki").exists())

    def test_symlinked_output_directory_escape_is_rejected_before_write(self) -> None:
        target = make_target()
        outside = Path(tempfile.mkdtemp(prefix="cca-outside-"))
        (target / "_runtime").mkdir()
        os.symlink(outside, target / "_runtime" / "operations")
        result = generate(target)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(outside.iterdir()), [])

    def test_output_specs_are_validated(self) -> None:
        cases = {
            "escape": {"slot": "system.operations", "file": "../paths.sh"},
            "durable": {"slot": "knowledge.durable", "file": "paths.sh"},
            "unknown": {"slot": "system.nowhere", "file": "paths.sh"},
        }
        for label, spec in cases.items():
            with self.subTest(label):
                target = make_target()
                data = load(target)
                data["generation_contract"]["outputs"]["paths"] = spec
                save(target, data)
                self.assertNotEqual(audit(target).returncode, 0)
                self.assertNotEqual(generate(target).returncode, 0)

    def test_bootstrap_anchor_cannot_move(self) -> None:
        target = make_target()
        set_binding(target, "workspace.schema", "_runtime/WORKSPACE.yaml")
        result = audit(target)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("only fixed bootstrap path", failures(result))

    def test_agents_binding_is_resolved_not_hardcoded(self) -> None:
        target = make_target()
        set_binding(target, "agent.instructions", "CONTROL.md")
        (target / "AGENTS.md").rename(target / "CONTROL.md")
        self.assertEqual(generate(target).returncode, 0)
        self.assertEqual(generate(target, "--check").returncode, 0)


class V3IdentityTests(unittest.TestCase):
    def test_identity_is_optional_and_rendered_from_schema(self) -> None:
        target = make_target()
        self.assertEqual(audit(target).returncode, 0)
        data = load(target)
        data["identity"] = {"endpoint": "brain://example", "owner": "human"}
        save(target, data)
        self.assertEqual(audit(target).returncode, 0, failures(audit(target)))
        self.assertEqual(generate(target).returncode, 0)
        for rel in ("CONTEXT.md", "_runtime/docs/SPEC.md"):
            text = (target / rel).read_text(encoding="utf-8")
            self.assertIn("brain://example", text, rel)
            self.assertIn("`identity` block of `WORKSPACE.yaml`", text, rel)

    def test_invalid_identity_fails(self) -> None:
        for identity in ({"endpoint": "00-wiki/meta/id.md", "owner": "human"}, {"endpoint": "brain://x", "owner": "derived"}, {"endpoint": "brain://x", "owner": "human", "path": "x"}):
            with self.subTest(identity):
                target = make_target()
                data = load(target)
                data["identity"] = identity
                save(target, data)
                self.assertNotEqual(audit(target).returncode, 0)


class V3SourceModelTests(unittest.TestCase):
    def collected(self, target: Path) -> Path:
        path = target / "20-sources" / "collected"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def test_human_markdown_clip_in_nested_container_passes(self) -> None:
        target = make_target()
        note = self.collected(target) / "clippings" / "ai" / "article.md"
        note.parent.mkdir(parents=True)
        note.write_text(clip(), encoding="utf-8")
        result = audit(target)
        self.assertEqual(result.returncode, 0, failures(result))

    def test_body_mutation_is_detected_but_frontmatter_edits_are_not_identity(self) -> None:
        target = make_target()
        note = self.collected(target) / "article.md"
        note.write_text(clip(), encoding="utf-8")
        note.write_text(note.read_text(encoding="utf-8").replace("tags:\n- clippings", "tags:\n- clippings\n- reviewed"), encoding="utf-8")
        self.assertEqual(audit(target).returncode, 0, failures(audit(target)))
        note.write_text(note.read_text(encoding="utf-8").replace("Article body.", "Rewritten body."), encoding="utf-8")
        result = audit(target)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("content hash mismatch (body)", failures(result))

    def test_web_clipper_source_alias_satisfies_origin(self) -> None:
        target = make_target()
        data = load(target)
        data["reference_contract"]["provenance"]["representations"]["markdown_frontmatter"]["field_aliases"] = {"origin": "source"}
        save(target, data)
        body = "Body.\n"
        prov = {"acquired_by": "human:owner", "acquisition_method": "obsidian-web-clipper", "acquired_at": "2026-10-30T12:00:00Z", "content_hash": body_hash(body)}
        front = yaml.safe_dump({"title": "T", "source": "https://example.com/x", "provenance": prov}, sort_keys=False)
        (self.collected(target) / "x.md").write_text(f"---\n{front}---\n{body}", encoding="utf-8")
        self.assertEqual(audit(target).returncode, 0, failures(audit(target)))

    def test_missing_or_dishonest_provenance_fails(self) -> None:
        cases = {
            "no frontmatter": "plain body\n",
            "no origin": clip(origin=""),
            "naive timestamp": clip(acquired_at="2026-10-30 12:00"),
            "unknown basis": clip(acquired_at_basis="guess"),
            "bad original time": clip(original_acquisition_time="sometime"),
            "wrong scope": clip(content_hash_scope="bytes"),
        }
        for label, text in cases.items():
            with self.subTest(label):
                target = make_target()
                (self.collected(target) / "x.md").write_text(text, encoding="utf-8")
                self.assertNotEqual(audit(target).returncode, 0)

    def test_honest_import_basis_passes(self) -> None:
        target = make_target()
        (self.collected(target) / "x.md").write_text(clip(acquired_at_basis="import", original_acquisition_time="unknown"), encoding="utf-8")
        self.assertEqual(audit(target).returncode, 0, failures(audit(target)))

    def test_binary_requires_sidecar_and_byte_hash(self) -> None:
        target = make_target()
        pdf = self.collected(target) / "papers" / "paper.pdf"
        pdf.parent.mkdir()
        pdf.write_bytes(b"%PDF evidence")
        self.assertNotEqual(audit(target).returncode, 0)
        meta = {"provenance": {"origin": "https://example.com/p.pdf", "acquired_by": "agent:crawler", "acquisition_method": "http-get", "acquired_at": "2026-10-30T12:00:00Z", "content_hash": "sha256:" + hashlib.sha256(b"%PDF evidence").hexdigest()}}
        (pdf.parent / "paper.pdf.source.yaml").write_text(yaml.safe_dump(meta), encoding="utf-8")
        self.assertEqual(audit(target).returncode, 0, failures(audit(target)))
        pdf.write_bytes(b"%PDF tampered")
        self.assertNotEqual(audit(target).returncode, 0)

    def test_directory_manifest_tree_identity_and_files_map(self) -> None:
        target = make_target()
        corpus = self.collected(target) / "upstream" / "corpus"
        (corpus / "sub").mkdir(parents=True)
        (corpus / "a.md").write_text("A [[link]]\n", encoding="utf-8")
        (corpus / "sub" / "b.png").write_bytes(b"\x89PNG")
        base = {"origin": "https://example.com/corpus", "acquired_by": "human:owner", "acquisition_method": "vault import", "acquired_at": "2026-09-26T15:04:42+02:00", "acquired_at_basis": "import", "original_acquisition_time": "unknown"}
        manifest = corpus / ".source.yaml"
        manifest.write_text(yaml.safe_dump({"provenance": {**base, "content_identity": provenance.tree_identity(corpus)}}), encoding="utf-8")
        self.assertEqual(audit(target).returncode, 0, failures(audit(target)))
        # coreutils recipe reproduces the identity
        recipe = run("bash", "-c", "find . -type f ! -path ./.source.yaml -printf '%P\\0' | LC_ALL=C sort -z | xargs -0 sha256sum | sha256sum", cwd=corpus)
        self.assertEqual("sha256-tree:" + recipe.stdout.split()[0], provenance.tree_identity(corpus))
        (corpus / "sub" / "b.png").write_bytes(b"changed")
        self.assertNotEqual(audit(target).returncode, 0)
        files = {rel: "sha256:" + hashlib.sha256((corpus / rel).read_bytes()).hexdigest() for rel in provenance.tree_files(corpus, ".source.yaml")}
        manifest.write_text(yaml.safe_dump({"provenance": {**base, "files": files}}), encoding="utf-8")
        self.assertEqual(audit(target).returncode, 0, failures(audit(target)))
        (corpus / "extra.md").write_text("unlisted\n", encoding="utf-8")
        self.assertNotEqual(audit(target).returncode, 0)

    def test_unverifiable_directory_identity_fails(self) -> None:
        target = make_target()
        corpus = self.collected(target) / "corpus"
        corpus.mkdir()
        (corpus / "a.md").write_text("A\n", encoding="utf-8")
        (corpus / ".source.yaml").write_text(yaml.safe_dump({"provenance": {"origin": "o", "acquired_by": "a", "acquisition_method": "m", "acquired_at": "2026-01-01T00:00:00Z", "content_identity": "sha256:abc recipe text"}}), encoding="utf-8")
        self.assertNotEqual(audit(target).returncode, 0)

    def test_orphan_sidecar_symlink_and_gitkeep(self) -> None:
        target = make_target()
        collected = self.collected(target)
        (collected / ".gitkeep").write_text("", encoding="utf-8")
        self.assertEqual(audit(target).returncode, 0, failures(audit(target)))
        (collected / "gone.pdf.source.yaml").write_text("provenance: {}\n", encoding="utf-8")
        self.assertNotEqual(audit(target).returncode, 0)
        (collected / "gone.pdf.source.yaml").unlink()
        os.symlink("/etc/hostname", collected / "linked.md")
        self.assertNotEqual(audit(target).returncode, 0)

    def test_curated_requires_provenance_and_curation_record(self) -> None:
        target = make_target()
        curated = target / "20-sources" / "curated"
        curated.mkdir(parents=True)
        (curated / "ref.md").write_text(clip(), encoding="utf-8")
        result = audit(target)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("curated_by", failures(result))
        (curated / "ref.md").write_text(clip(curated_by="human:owner", curated_at="2026-11-01T10:00:00+01:00"), encoding="utf-8")
        self.assertEqual(audit(target).returncode, 0, failures(audit(target)))

    def test_classification_is_actor_independent(self) -> None:
        for actor in ("human:owner", "agent:symbiont", "crawler:vacuum", "integration:rss"):
            with self.subTest(actor):
                target = make_target()
                (self.collected(target) / "x.md").write_text(clip(acquired_by=actor), encoding="utf-8")
                self.assertEqual(audit(target).returncode, 0, failures(audit(target)))

    def test_stamp_adds_body_hash_once_and_never_overwrites(self) -> None:
        target = make_target()
        body = "Clipped text with <% tp.date.now() %> literal.\n"
        front = yaml.safe_dump({"title": "T", "provenance": {"origin": "https://e.x/a", "acquired_by": "human:owner", "acquisition_method": "obsidian-web-clipper", "acquired_at": "2026-10-30T12:00:00+01:00"}}, sort_keys=False)
        note = self.collected(target) / "clippings" / "a.md"
        note.parent.mkdir()
        note.write_text(f"---\n{front}---\n{body}", encoding="utf-8")
        self.assertNotEqual(audit(target).returncode, 0)
        stamped = run(sys.executable, str(PACKAGE / "provenance.py"), "--target", str(target), "stamp", "20-sources/collected/clippings")
        self.assertEqual(stamped.returncode, 0, failures(stamped))
        self.assertIn("stamped: 1", stamped.stdout)
        self.assertTrue(note.read_text(encoding="utf-8").endswith(body))
        self.assertEqual(audit(target).returncode, 0, failures(audit(target)))
        note.write_text(note.read_text(encoding="utf-8").replace("literal", "edited"), encoding="utf-8")
        again = run(sys.executable, str(PACKAGE / "provenance.py"), "--target", str(target), "stamp", "20-sources/collected/clippings")
        self.assertIn("already-stamped: 1", again.stdout)
        self.assertNotEqual(audit(target).returncode, 0, "stamping must never launder a body mutation")

    def test_stamp_refuses_paths_outside_reference_classes(self) -> None:
        target = make_target()
        (target / "00-wiki").mkdir()
        result = run(sys.executable, str(PACKAGE / "provenance.py"), "--target", str(target), "stamp", "00-wiki")
        self.assertNotEqual(result.returncode, 0)


class V3StateAssetArchiveTests(unittest.TestCase):
    def test_hotset_is_recognized_while_specific_state_bindings_win(self) -> None:
        data = schema_module.load_schema(PACKAGE / "WORKSPACE.yaml")
        resolve = lambda p: schema_module.resolve_slot_for_path(p, data)["key"]  # noqa: E731
        self.assertEqual(resolve("_state/Dashboard.canvas"), "state.hotset")
        self.assertEqual(resolve("_state/bookmarks/Daily.md"), "state.hotset")
        self.assertEqual(resolve("_state/NOW.md"), "state.current")
        self.assertEqual(resolve("_state/tasks/t.md"), "state.tasks")
        hotset = next(s for s in data["slots"] if s["key"] == "state.hotset")
        ops = schema_module.effective_agent_operations(hotset, data)
        self.assertIn("edit", ops)
        self.assertNotIn("delete", ops)

    def test_human_templates_are_distinct_from_system_templates(self) -> None:
        data = schema_module.load_schema(PACKAGE / "WORKSPACE.yaml")
        resolve = lambda p: schema_module.resolve_slot_for_path(p, data)["key"]  # noqa: E731
        self.assertEqual(resolve("_assets/templates/note.md"), "asset.templates")
        self.assertEqual(resolve("_assets/attachments/a.png"), "asset.library")
        self.assertEqual(resolve("_runtime/templates/knowledge.md"), "system.templates")
        for key in ("asset.library", "asset.templates"):
            slot = next(s for s in data["slots"] if s["key"] == key)
            self.assertEqual(schema_module.effective_agent_operations(slot, data), ["read"])

    def test_promotion_is_a_human_authorized_operation(self) -> None:
        data = schema_module.load_schema(PACKAGE / "WORKSPACE.yaml")
        collected = next(s for s in data["slots"] if s["key"] == "reference.collected")
        self.assertIn("promotion (human-authorized)", schema_module.effective_agent_operations(collected, data))

    def test_cold_storage_needs_no_manifest_but_retirement_manifests_are_validated(self) -> None:
        target = make_target()
        archive = target / "90-archive"
        (archive / "Old Meetings").mkdir(parents=True)
        (archive / "Old Meetings" / "notes.md").write_text("cold\n", encoding="utf-8")
        (archive / "dump.7z").write_bytes(b"7z")
        self.assertEqual(audit(target).returncode, 0, failures(audit(target)))
        retired = archive / "project-x"
        retired.mkdir()
        manifest = {"source_key": "project.notes", "semantic_role": "work.project", "boundary": "project-x", "boundary_class": "project.notes", "original_binding": "40-projects/notes/project-x/", "archived_at": "2026-11-01T10:00:00+01:00", "archived_by": "human:owner"}
        (retired / ".archive.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
        self.assertEqual(audit(target).returncode, 0, failures(audit(target)))
        for field, value in (("archived_at", "yesterday"), ("source_key", "not.a.key"), ("archived_by", "")):
            with self.subTest(field):
                (retired / ".archive.yaml").write_text(yaml.safe_dump({**manifest, field: value}), encoding="utf-8")
                self.assertNotEqual(audit(target).returncode, 0)


class V2CompatibilityTests(unittest.TestCase):
    def test_v2_fixture_still_validates_and_generates_root_helpers(self) -> None:
        target = make_target(V2)
        self.assertEqual(load(target)["schema_version"], 2)
        self.assertEqual(generate(target).returncode, 0)
        self.assertEqual(generate(target, "--check").returncode, 0)
        for name in ("paths.sh", "mkdirs.sh", "obsidian-excludes.txt", "SPEC.md", "CONTEXT.md"):
            self.assertTrue((target / name).is_file(), name)
        self.assertIn('WS_ROOT="$(cd -- "$(dirname -- "$_ws_self")" && pwd)"', (target / "paths.sh").read_text(encoding="utf-8"))

    def test_v2_keeps_v2_reference_semantics(self) -> None:
        target = make_target(V2)
        (target / "20-sources" / "collected").mkdir(parents=True)
        (target / "20-sources" / "collected" / "clip.md").write_text(clip(), encoding="utf-8")
        # v2 requires a .source.yaml sidecar even for Markdown; frontmatter provenance is a v3 feature.
        result = audit(target)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing provenance sidecar", failures(result))

    def test_v3_semantics_are_not_accepted_under_a_v2_declaration(self) -> None:
        target = make_target()
        data = load(target)
        data["schema_version"] = 2
        save(target, data)
        self.assertNotEqual(audit(target).returncode, 0)

    def test_unsupported_schema_version_fails(self) -> None:
        target = make_target()
        data = load(target)
        data["schema_version"] = 4
        save(target, data)
        self.assertIn("schema_version must be 2 or 3", failures(audit(target)))


class ReviewRegressionTests(unittest.TestCase):
    """Regressions for the independent review of the first v3 cut."""

    def collected(self, target: Path) -> Path:
        path = target / "20-sources" / "collected"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def stamp(self, target: Path, *paths: str) -> subprocess.CompletedProcess[str]:
        return run(sys.executable, str(PACKAGE / "provenance.py"), "--target", str(target), "stamp", *paths)

    def test_stamp_requires_explicit_paths_and_never_touches_curated(self) -> None:
        target = make_target()
        curated = target / "20-sources" / "curated"
        curated.mkdir(parents=True)
        text = "---\nprovenance:\n  origin: o\n  acquired_by: a\n  acquisition_method: m\n  acquired_at: '2026-01-01T00:00:00Z'\n---\nbody\n"
        (curated / "c.md").write_text(text, encoding="utf-8")
        self.assertNotEqual(self.stamp(target).returncode, 0)
        refused = self.stamp(target, "20-sources/curated")
        self.assertNotEqual(refused.returncode, 0)
        self.assertEqual((curated / "c.md").read_text(encoding="utf-8"), text)

    def test_stamp_flat_fields_from_capture_tool(self) -> None:
        target = make_target()
        body = "Body.\n"
        note = self.collected(target) / "flat.md"
        note.write_text("---\ntitle: T\norigin: https://e.x/a\nacquired_by: human:owner\nacquisition_method: obsidian-web-clipper\nacquired_at: 2026-10-30T12:00:00+01:00\ntags:\n  - clippings\n---\n" + body, encoding="utf-8")
        self.assertEqual(self.stamp(target, "20-sources/collected/flat.md").returncode, 0)
        self.assertTrue(note.read_text(encoding="utf-8").endswith(body))
        self.assertEqual(audit(target).returncode, 0, failures(audit(target)))

    def test_stamp_handles_nested_mappings_and_refuses_unsafe_layouts(self) -> None:
        target = make_target()
        nested = self.collected(target) / "nested.md"
        nested.write_text("---\nprovenance:\n  origin: o\n  extra:\n    sub: 1\n  acquired_by: a\n  acquisition_method: m\n  acquired_at: '2026-01-01T00:00:00Z'\n---\nbody\n", encoding="utf-8")
        self.assertEqual(self.stamp(target, "20-sources/collected/nested.md").returncode, 0)
        self.assertEqual(audit(target).returncode, 0, failures(audit(target)))
        for label, front in (("flow", "provenance: {origin: o, acquired_by: a, acquisition_method: m, acquired_at: '2026-01-01T00:00:00Z'}"),
                             ("comment", "provenance:  # note\n  origin: o\n  acquired_by: a\n  acquisition_method: m\n  acquired_at: '2026-01-01T00:00:00Z'"),
                             ("incomplete", "provenance:\n  origin: o")):
            with self.subTest(label):
                note = self.collected(target) / f"{label}.md"
                original = f"---\n{front}\n---\nbody\n"
                note.write_text(original, encoding="utf-8")
                result = self.stamp(target, f"20-sources/collected/{label}.md")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(note.read_text(encoding="utf-8"), original)

    def test_stamp_refuses_collected_binding_that_escapes(self) -> None:
        target = make_target()
        outside = Path(tempfile.mkdtemp(prefix="cca-outside-"))
        (outside / "x.md").write_text("---\nprovenance:\n  origin: o\n  acquired_by: a\n  acquisition_method: m\n  acquired_at: '2026-01-01T00:00:00Z'\n---\nb\n", encoding="utf-8")
        (target / "20-sources").mkdir()
        os.symlink(outside, target / "20-sources" / "collected")
        self.assertNotEqual(self.stamp(target, "20-sources/collected/x.md").returncode, 0)
        self.assertNotIn("content_hash", (outside / "x.md").read_text(encoding="utf-8"))

    def test_outputs_cannot_target_human_bindings_or_overwrite_human_files(self) -> None:
        for slot in ("system.templates", "system.workflows", "agent.skills", "asset.templates"):
            with self.subTest(slot):
                target = make_target()
                data = load(target)
                data["generation_contract"]["outputs"]["spec"] = {"slot": slot, "file": "SPEC.md"}
                save(target, data)
                self.assertNotEqual(audit(target).returncode, 0)
        target = make_target()
        data = load(target)
        data["generation_contract"]["outputs"]["spec"] = {"slot": "system.documentation", "file": "HOW-TO.md"}
        save(target, data)
        (target / "_runtime" / "docs").mkdir(parents=True)
        (target / "_runtime" / "docs" / "HOW-TO.md").write_text("# Human guide\n", encoding="utf-8")
        result = generate(target)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((target / "_runtime" / "docs" / "HOW-TO.md").read_text(encoding="utf-8"), "# Human guide\n")

    def test_output_must_be_governed_by_its_declared_slot_and_not_collide(self) -> None:
        cases = {
            "nested under durable": lambda d: next(s for s in d["slots"] if s["key"] == "system.operations").__setitem__("binding", "00-wiki/ops/"),
            "case-fold collision": lambda d: d["generation_contract"]["outputs"].__setitem__("mkdirs", {"slot": "system.operations", "file": "PATHS.sh"}),
        }
        for label, mutate in cases.items():
            with self.subTest(label):
                target = make_target()
                data = load(target)
                mutate(data)
                save(target, data)
                self.assertNotEqual(audit(target).returncode, 0)

    def test_dot_segment_bindings_are_rejected(self) -> None:
        for binding in ("./", "_runtime/./operations/", "a//b/"):
            with self.subTest(binding):
                self.assertIsNotNone(schema_module.validate_binding_text(binding))
                target = make_target()
                set_binding(target, "system.operations", binding)
                self.assertNotEqual(audit(target).returncode, 0)

    def test_helper_copied_into_another_anchored_workspace_fails_closed(self) -> None:
        target = make_target()
        self.assertEqual(generate(target).returncode, 0)
        victim = make_target()
        (victim / "x" / "y").mkdir(parents=True)
        shutil.copy2(target / "_runtime/operations/mkdirs.sh", victim / "x" / "y" / "mkdirs.sh")
        # victim/x/y/../.. is victim, which has a WORKSPACE.yaml but not this helper.
        result = run("bash", str(victim / "x" / "y" / "mkdirs.sh"), "--all")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((victim / "00-wiki").exists())

    def test_symlinked_helper_resolves_its_own_workspace(self) -> None:
        inner = make_target()
        self.assertEqual(generate(inner).returncode, 0)
        outer = make_target()
        (outer / "projects" / "inner").mkdir(parents=True)
        os.symlink(inner / "_runtime/operations/paths.sh", outer / "projects" / "inner" / "paths.sh")
        result = run("bash", "-c", f'source "{outer}/projects/inner/paths.sh" && echo "$WS_ROOT"')
        self.assertEqual(result.returncode, 0, failures(result))
        self.assertEqual(Path(result.stdout.strip()), inner.resolve())

    def test_failed_source_leaves_no_wrong_root(self) -> None:
        target = make_target()
        self.assertEqual(generate(target).returncode, 0)
        stray = Path(tempfile.mkdtemp(prefix="cca-stray-")) / "a" / "b"
        stray.mkdir(parents=True)
        shutil.copy2(target / "_runtime/operations/paths.sh", stray / "paths.sh")
        result = run("bash", "-c", f'source "{stray}/paths.sh"; echo "rc=$? root=${{WS_ROOT:-unset}}"')
        self.assertIn("rc=1 root=unset", result.stdout)

    def test_paths_with_spaces(self) -> None:
        base = Path(tempfile.mkdtemp(prefix="cca space "))
        target = base / "my workspace"
        target.mkdir()
        for name in ("WORKSPACE.yaml", "AGENTS.md"):
            shutil.copy2(PACKAGE / name, target / name)
        self.assertEqual(generate(target).returncode, 0)
        result = run("bash", "-c", f'source "{target}/_runtime/operations/paths.sh" && echo "$WS_ROOT"')
        self.assertEqual(Path(result.stdout.strip()), target.resolve())

    def test_manifest_named_directory_and_os_noise(self) -> None:
        target = make_target()
        corpus = self.collected(target) / "c"
        (corpus / ".source.yaml").mkdir(parents=True)
        (corpus / ".source.yaml" / "hidden.md").write_text("x\n", encoding="utf-8")
        self.assertNotEqual(audit(target).returncode, 0)
        shutil.rmtree(corpus)
        (self.collected(target) / ".DS_Store").write_bytes(b"\x00")
        self.assertEqual(audit(target).returncode, 0, failures(audit(target)))

    def test_original_time_precision_and_bare_date_acquired_at(self) -> None:
        target = make_target()
        (self.collected(target) / "d.md").write_text(clip(original_acquisition_time="2025-07-05"), encoding="utf-8")
        self.assertEqual(audit(target).returncode, 0, failures(audit(target)))
        (self.collected(target) / "d.md").write_text(clip(acquired_at="2025-07-05"), encoding="utf-8")
        self.assertIn("a bare date is not a timestamp", failures(audit(target)))

    def test_curated_migration_basis_is_honest_and_validated(self) -> None:
        target = make_target()
        curated = target / "20-sources" / "curated"
        curated.mkdir(parents=True)
        (curated / "r.md").write_text(clip(curated_by="human:owner", curated_at="2026-11-01T10:00:00+01:00", curated_at_basis="migration"), encoding="utf-8")
        self.assertEqual(audit(target).returncode, 0, failures(audit(target)))
        (curated / "r.md").write_text(clip(curated_by="human:owner", curated_at="2026-11-01T10:00:00+01:00", curated_at_basis="guess"), encoding="utf-8")
        self.assertNotEqual(audit(target).returncode, 0)

    def test_v3_requires_cca_1_3_0(self) -> None:
        target = make_target()
        data = load(target)
        data["cca"]["specification"] = "1.0.0"
        save(target, data)
        self.assertIn("requires cca.specification >= 1.3.0", failures(audit(target)))

    def test_hotset_is_in_the_human_search_surface(self) -> None:
        target = make_target()
        self.assertEqual(generate(target).returncode, 0)
        excludes = (target / "_runtime/operations/obsidian-excludes.txt").read_text(encoding="utf-8").splitlines()
        self.assertNotIn("_state/", excludes)
        self.assertIn("_state/NOW.md", excludes)
        self.assertIn("_state/tasks/", excludes)


if __name__ == "__main__":
    unittest.main()
