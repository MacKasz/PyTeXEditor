import pytest # noqa F401
from PyTeXEditor.TextEdit import TextEdit
from PyTeXEditor.Sidebar import Sidebar


def test_sanity():
    print("Run")


def test_send_hide(qtbot):
    """Check if signals are sent from the textedit
    """
    textedit = TextEdit()

    with qtbot.waitSignal(textedit.sidebar_visable_signal, timeout=100,
                          raising=True):
        textedit.hide_sidebar()

    with qtbot.waitSignal(textedit.sidebar_visable_signal, timeout=100,
                          raising=True):
        textedit.show_sidebar()


def test_sidebar_hide(qtbot):
    """Check if the sidebar reacts upon reciving hide or show signal
    """
    textedit = TextEdit()
    sidebar = Sidebar()
    textedit.sidebar_visable_signal.connect(sidebar.setVisible)

    qtbot.addWidget(textedit)
    qtbot.addWidget(sidebar)

    with qtbot.waitSignal(textedit.sidebar_visable_signal, timeout=100,
                          raising=True):
        textedit.hide_sidebar()

    assert sidebar.isVisible() is False

    with qtbot.waitSignal(textedit.sidebar_visable_signal, timeout=100,
                          raising=True):
        textedit.show_sidebar()

    assert sidebar.isVisible() is True
