# ICM parity capability suite

This suite defines the granular behavioral contracts required before CCA may claim that native ICM behavior is preserved at least at parity. It is intentionally more granular than the 14-case interoperability suite.

`capabilities.json` is the source catalog for the final neutral audit. Each capability must be instantiated as an isolated behavioral case against three arms where applicable: pinned ICM, CCA, and no-skill control. The same model/runtime/budget/fixture must be used for every arm.

A capability inherited from ICM is classified **PARITY**, **IMPROVEMENT**, or **REGRESSION** for CCA. It is not an "ICM-only win" merely because ICM originated it. A=B=C indicates the case may be testing generic model competence rather than architectural contribution.

The final compound builder case must exercise discovery through validation plus setup/status/fresh-agent use; atomic passes alone are not sufficient.
