import pytest
from mrrobot.util import get_brainly_task, BrainlyRequestFailedException, BrainlyTaskDoesNotExistException


async def test_get_brainly_task():
    TEST_BRAINLY_TASK_ID = 2
    TEST_BRAINLY_TASK_LINK = "https://znanija.com/task/2"

    task = await get_brainly_task(TEST_BRAINLY_TASK_ID)

    assert isinstance(task, dict)
    assert task.get("id") == TEST_BRAINLY_TASK_ID
    assert task.get("subject") is None or isinstance(task["subject"], str)
    assert task.get("link") == TEST_BRAINLY_TASK_LINK
    assert isinstance(task["created"], str)
    assert isinstance(task["answers_count"], int)
    assert isinstance(task["short_content"], str)


async def test_get_brainly_task_by_invalid_id():
    with pytest.raises(BrainlyRequestFailedException):
        await get_brainly_task(-1)


async def test_get_brainly_task_that_does_not_exist():
    TEST_TASK_ID = 9999999999

    with pytest.raises(BrainlyTaskDoesNotExistException):
        await get_brainly_task(TEST_TASK_ID)
