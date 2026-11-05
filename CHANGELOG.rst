
Changelog
=========

Unreleased
----------

- Target pyGAPS 5.
- Require Python 3.10 or newer.
- Fix deleting last isotherm, clearing its metadata and graph, and deleting
  with no selection.
- Propagate unexpected analysis errors instead of suppressing them, preserve
  calculation warnings on failure, and escape log messages for both themes.
- Disable saving and exporting until an analysis has a valid result, and
  invalidate stale results after failed recalculation or changed inputs.
- Support XLSX loading and saving; retain legacy XLS reading only.
- Continue file batches after errors, filter folder imports, accept uppercase
  extensions, and remember successful commercial imports with their settings.
- Infer missing save suffixes from the selected format, report write failures,
  and remember the results export directory.
- Avoid forwarding handled copy shortcuts to the point editor's base widget.
- Restyle existing plots, legends, fit lines and model-isotherm list entries
  when switching themes, while preserving graph data and zoom. Show the selected
  theme in the menu.
- Pin CI tests and bundles to the same pyGAPS development commit.
- Confirm replacement of existing files after inferring a missing save suffix.
- Preserve multi-isotherm zoom and semantic marker colours during theme changes.
- Invalidate results after changes to PSD options, IAST tables and composition,
  model-guess candidates, alpha-s inputs, and isosteric point counts.
- Fix IAST range generation on current pandas versions and point-count editing
  for isosteric calculations.

0.5.0 (2022-03-13)
------------------

- Improved information display and error criteria in mesoporous PSD calculations.

- Fixed a bug that made aliases not clear in the Adsorbate explorer.

0.5.0 (2022-03-13)
------------------

- Added recently opened files.
