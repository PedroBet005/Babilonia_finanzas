import pytest

from domain.entities.category import Category


def test_category_name_required():
    with pytest.raises(ValueError, match="category_name_required"):
        Category(name="")


def test_category_name_is_stripped():
    category = Category(name="  Food  ")

    assert category.name == "Food"


def test_category_equality_is_case_insensitive():
    c1 = Category(name="Food")
    c2 = Category(name="food")

    assert c1 == c2


def test_category_can_be_used_in_set():
    categories = {
        Category(name="Food"),
        Category(name="food"),
        Category(name="FOOD"),
    }

    assert len(categories) == 1
