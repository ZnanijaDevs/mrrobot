import pytest
from typing import Callable, Any
from mrrobot.util import get_deletion_reason, find_profile_link, find_task_id, \
    find_user_id_in_profile_link


def assert_test_cases(test_cases: dict[Any], test_func: Callable[[str], Any]):
    for arg, value in test_cases.items():
        result = test_func(arg)

        if value is None:
            assert result is None
        else:
            assert value == result


def test_get_deletion_reason():
    test_cases = {
        "<https://znanija.com/profil/andrewss-3939548> Спам": "Спам",
        "<https://znanija.com/profil/nick1-13|контент>": "Контент",
        "18+ <https://znanija.com/users/user_content/1248544>": "18+",
        "СПаММ!!! <https://znanija.com/users/redirect_user/122>": "Спамм!!!",
        "": None,
        "<https://znanija.com/users/redirect_user/1>": None
    }

    assert_test_cases(test_cases, get_deletion_reason)


def test_find_profile_link():
    test_cases = {
        "<https://znanija.com/profil/madiabdimalik2021ff-27088247> СпАМ": "https://znanija.com/profil/madiabdimalik2021ff-27088247",
        "<https://znanija.com/app/profile/4234235|18+>": "https://znanija.com/app/profile/4234235",
        "Reason <https://znanija.com/users/redirect_user/12>": "https://znanija.com/users/redirect_user/12",
        "Reason 1 <https://znanija.com/users/user_content/28605650|Reason 2>": "https://znanija.com/users/user_content/28605650",
        "": None,
        "no link": None,
        "<https://example.com|Link>": None,
        "Reason <https://znanija.com/proflic/testuser-1>": None,
        "<https://znanija.com/profil/maa--1>": None
    }

    assert_test_cases(test_cases, find_profile_link)


def test_find_task_id():
    test_cases = {
        "<https://znanija.com/task/2358423|Message>": 2358423,
        "Text... <https://znanija.com/task/65454546>": 65454546,
        "<https://znanija.com/task/465546> test": 465546,
        "<https://znanija.com/taskd/345435> text": None,
        "": None
    }

    assert_test_cases(test_cases, find_task_id)


def test_find_user_id_in_profile_link():
    test_cases = {
        "https://znanija.com/profil/alypkashevilan-28605651": 28605651,
        "https://znanija.com/users/redirect_user/63543": 63543,
        "https://znanija.com/users/user_content/4359345": 4359345,
    }

    assert_test_cases(test_cases, find_user_id_in_profile_link)

    with pytest.raises(ValueError):
        find_user_id_in_profile_link("")
        find_user_id_in_profile_link("https://znanija.com/users/user_content/-3434")
