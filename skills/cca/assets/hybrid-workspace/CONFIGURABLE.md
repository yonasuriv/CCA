# Configurable workspace (v5, opt-in)

Use lowercase workspace.yaml. The bundled workspace.schema.json validates the shape; configurable.py validates policy and references. Built-in roles inherit their security policy, but binding keys and paths are owner-defined. Unknown roles require explicit policy fields. The reference corpus is an optional capability with three dependent roles. Outputs declare a renderer and destination slot; deleting an output never deletes its old file.

For existing v3/v4 workspaces, run `python resolve.py --target <root> --migrate-v5` to print a candidate. Review it before replacing workspace.yaml. No filesystem content is moved. Run audit.py and generate.py --check against a copy first. Existing v2-v4 profiles remain unchanged. See workspace.example.yaml for a minimal example.

This is an experimental profile pending regression and migration review. It does not automatically rewrite external references or remove obsolete artifacts.
