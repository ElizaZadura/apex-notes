"""Main application window wiring menus, tabs, and split panes."""
from __future__ import annotations

from pathlib import Path
from typing import Optional, cast

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QFileDialog, QMainWindow,
                               QMessageBox, QSplitter, QWidget)

from src.core.document_manager import DocumentManager
from src.ui.tabbed_pane import TabbedPane


class MainWindow(QMainWindow):
    """Application shell defining menu actions and the split layout."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Apex Notepad")
        self.resize(1200, 720)

        self._manager = DocumentManager()
        self._splitter = QSplitter(Qt.Horizontal, self)
        self._panes: list[TabbedPane] = [TabbedPane(self._manager), TabbedPane(self._manager)]
        self._splitter.addWidget(self._panes[0])
        self._splitter.addWidget(self._panes[1])
        self._splitter.setStretchFactor(0, 1)
        self._splitter.setStretchFactor(1, 1)
        self.setCentralWidget(self._splitter)
        self._panes[1].setVisible(False)

        self._active_index = 0

        self._wire_pane_signals()
        self._create_actions()
        self._create_menus()

        self._apply_split_orientation(True)
        self._create_initial_document()
        self._install_focus_tracking()

    def _create_initial_document(self) -> None:
        doc_id = self._manager.create_document()
        self._panes[self._active_index].add_document(doc_id)

    # region Menu creation
    def _create_actions(self) -> None:
        self._new_action = QAction("New", self)
        self._new_action.setShortcut("Ctrl+N")
        self._new_action.triggered.connect(self._handle_new_document)

        self._open_action = QAction("Open…", self)
        self._open_action.setShortcut("Ctrl+O")
        self._open_action.triggered.connect(self._handle_open_document)

        self._save_action = QAction("Save", self)
        self._save_action.setShortcut("Ctrl+S")
        self._save_action.triggered.connect(self._handle_save_document)

        self._save_as_action = QAction("Save As…", self)
        self._save_as_action.setShortcut("Ctrl+Shift+S")
        self._save_as_action.triggered.connect(lambda: self._handle_save_document(save_as=True))

        self._toggle_split_action = QAction("Toggle Second Pane", self)
        self._toggle_split_action.setShortcut("Ctrl+Alt+Shift+H")
        self._toggle_split_action.setCheckable(True)
        self._toggle_split_action.triggered.connect(self._toggle_second_pane)

        self._orientation_action = QAction("Horizontal Split", self)
        self._orientation_action.setShortcut("Ctrl+Alt+H")
        self._orientation_action.setCheckable(True)
        self._orientation_action.setChecked(True)
        self._orientation_action.toggled.connect(self._apply_split_orientation)

    def _create_menus(self) -> None:
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(self._new_action)
        file_menu.addAction(self._open_action)
        file_menu.addSeparator()
        file_menu.addAction(self._save_action)
        file_menu.addAction(self._save_as_action)

        view_menu = menu_bar.addMenu("View")
        view_menu.addAction(self._orientation_action)
        view_menu.addAction(self._toggle_split_action)
    # endregion

    # region Document commands
    def _active_pane(self) -> TabbedPane:
        pane = self._panes[self._active_index]
        if not pane.isVisible():
            # default to first visible pane
            pane = self._panes[0] if self._panes[0].isVisible() else self._panes[1]
            self._active_index = self._panes.index(pane)
        return pane

    def _handle_new_document(self) -> None:
        doc_id = self._manager.create_document()
        self._active_pane().add_document(doc_id)

    def _handle_open_document(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", str(Path.cwd()))
        if not file_path:
            return
        doc_id = self._manager.load_from_disk(Path(file_path))
        self._active_pane().add_document(doc_id)

    def _handle_save_document(self, *, save_as: bool = False) -> None:
        pane = self._active_pane()
        document_id = pane.current_document_id()
        if document_id is None:
            return
        document = self._manager.get_document(document_id)

        target_path: Optional[Path] = document.path
        if save_as or target_path is None:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", document.display_name())
            if not file_path:
                return
            target_path = Path(file_path)

        try:
            self._manager.save_to_disk(document_id, target_path)
        except OSError as exc:
            QMessageBox.critical(self, "Save Failed", str(exc))
            return

        for pane in self._panes:
            pane.refresh_tab_title(document_id)
    # endregion

    # region Split management
    def _toggle_second_pane(self, checked: bool) -> None:
        self._panes[1].setVisible(checked)
        if checked and self._panes[1].current_document_id() is None:
            doc_id = self._manager.create_document()
            self._panes[1].add_document(doc_id)
        self._splitter.setSizes([1, 1])

    def _apply_split_orientation(self, horizontal: bool) -> None:
        orientation = Qt.Horizontal if horizontal else Qt.Vertical
        self._splitter.setOrientation(orientation)
        self._splitter.setSizes([1, 1])
        label = "Horizontal Split" if horizontal else "Vertical Split"
        self._orientation_action.blockSignals(True)
        self._orientation_action.setChecked(horizontal)
        self._orientation_action.setText(label)
        self._orientation_action.blockSignals(False)

    def focusInEvent(self, event) -> None:  # type: ignore[override]
        super().focusInEvent(event)
        self._update_active_pane_from_focus()

    def _install_focus_tracking(self) -> None:
        app = QApplication.instance()
        if app is None:
            return
        qt_app = cast(QApplication, app)
        qt_app.focusChanged.connect(self._handle_focus_changed)

    def _wire_pane_signals(self) -> None:
        for index, pane in enumerate(self._panes):
            pane.became_empty.connect(self._make_pane_empty_handler(index))

    def _handle_focus_changed(self, _old: QWidget | None, new: QWidget | None) -> None:
        if new is None:
            return
        for index, pane in enumerate(self._panes):
            if not pane.isVisible():
                continue
            if pane.isAncestorOf(new) or pane is new:
                self._active_index = index
                break

    def _make_pane_empty_handler(self, index: int):
        def handler() -> None:
            self._handle_pane_empty(index)
        return handler

    def _update_active_pane_from_focus(self) -> None:
        focused = self.focusWidget()
        for index, pane in enumerate(self._panes):
            if not pane.isVisible():
                continue
            if pane.isAncestorOf(focused):
                self._active_index = index
                break
        else:
            self._active_index = 0

    def _handle_pane_empty(self, index: int) -> None:
        if index == 0:
            # Always keep at least one document available.
            doc_id = self._manager.create_document()
            self._panes[0].add_document(doc_id)
            self._active_index = 0
            return

        pane = self._panes[index]
        pane.setVisible(False)
        self._splitter.setSizes([1, 0])
        self._toggle_split_action.blockSignals(True)
        self._toggle_split_action.setChecked(False)
        self._toggle_split_action.blockSignals(False)
        self._active_index = 0
    # endregion
