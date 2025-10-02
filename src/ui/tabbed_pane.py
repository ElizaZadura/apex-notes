"""Tabbed pane widget managing documents within a splitter cell."""
from __future__ import annotations

from typing import Dict, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from src.core.document import Document
from src.core.document_manager import DocumentManager
from src.ui.editor_widget import EditorWidget


class TabbedPane(QWidget):
    """Container providing tabbed access to multiple documents."""

    became_empty = Signal()

    def __init__(self, manager: DocumentManager, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._manager = manager
        self._binders: Dict[int, EditorWidget] = {}
        self._tab = QTabWidget(self)
        self._tab.setTabsClosable(True)
        self._tab.setMovable(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._tab)

        self._tab.tabCloseRequested.connect(self._close_tab)

    def add_document(self, document_id: int) -> None:
        document = self._manager.get_document(document_id)
        editor = EditorWidget(document=document)
        self._binders[document_id] = editor
        index = self._tab.addTab(editor, document.display_name())
        self._tab.setCurrentIndex(index)
        editor.content_modified.connect(lambda: self.refresh_tab_title(document_id))
        if self._tab.count() == 1:
            # ensure first document reflects clean state when just opened
            self.refresh_tab_title(document_id)

    def current_document_id(self) -> Optional[int]:
        widget = self._tab.currentWidget()
        if widget is None:
            return None
        for doc_id, editor in self._binders.items():
            if editor is widget:
                return doc_id
        return None

    def _close_tab(self, index: int) -> None:
        widget = self._tab.widget(index)
        if widget is None:
            return
        for doc_id, editor in list(self._binders.items()):
            if editor is widget:
                self._tab.removeTab(index)
                self._binders.pop(doc_id)
                self._manager.close_document(doc_id)
                if self._tab.count() == 0:
                    self.became_empty.emit()
                break

    def document_ids(self) -> list[int]:
        return list(self._binders.keys())

    def is_empty(self) -> bool:
        return self._tab.count() == 0

    def refresh_tab_title(self, document_id: int) -> None:
        document = self._manager.get_document(document_id)
        editor = self._binders.get(document_id)
        if editor is None:
            return
        index = self._tab.indexOf(editor)
        if index >= 0:
            title = document.display_name()
            if document.is_dirty:
                title = f"* {title}"
            self._tab.setTabText(index, title)
