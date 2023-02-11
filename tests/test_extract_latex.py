import pytest  # noqa F401
from PyTeXEditor.extract_latex import delete_comments, seperate


def test_delete_comment():
    assert delete_comments("word1 word2") == "word1 word2"

    assert delete_comments("word1 % word2") == "word1 "

    assert delete_comments("word1 % word2 % word3") == "word1 "


def test_seperate():

    assert seperate(["asd asd"]) == ["asd asd"]

    assert seperate(["asd", "asd"]) == ["asd asd"]

    assert seperate(["\\item item1 \\item item2"]) == \
           seperate(["\\item", "item1", "\\item item2"])
