# 📝 Apex Notepad v0.1 Issue List

## Core usability
- [ ] Implement autosave with configurable interval (`settings.json`).
- [ ] Show `*` in tab title when document is dirty; clear on save.
- [ ] Restore last session (open tabs, split layout, cursors) on startup.

## Keymap + commands
- [ ] Load default keymap and merge with `~/.apex/keymap.json`.
- [ ] Add common shortcuts: `Ctrl+N/O/S/W`, `Ctrl+Tab`, `Ctrl+Shift+Tab`, `F11` (toggle split).
- [ ] Provide “Reset keymap” command.

## MacroEngine
- [ ] Discover macros from `~/.apex/macros/*.py`.
- [ ] Add “Run Macro…” menu entry to select + execute.
- [ ] Sandbox macros (no network/fs by default).

## Settings & config
- [ ] Read/write `~/.apex/settings.json` (theme, font, autosave interval).
- [ ] Add “Preferences” menu entry opening settings file directly.

## Testing + infra
- [ ] Add `tests/` folder with pytest.
- [ ] Smoke test: create → type → autosave → close → restore.
- [ ] Smoke test: keymap merge with user JSON.
- [ ] CI job: run `make test`.
