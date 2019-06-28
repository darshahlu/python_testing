# See https://stackoverflow.com/questions/49271586/valueerror-wrapper-loop-when-unwrapping
# "from unittest.mock import Mock, call" causes ValueError: wrapper loop when unwrapping call!
from unittest import mock
import time

import pytest

from example.example_library.retry import retry
from example.example_library.retry import LOGGER


def test_retry_exhaustion(monkeypatch, caplog):
    caplog.set_level("DEBUG", logger=LOGGER.name)
    monkeypatch.setattr(time, "sleep", mock.Mock())

    my_listener = mock.Mock(
        side_effect=[
            KeyError("exception 1"),
            KeyError("exception 2"),
            KeyError("exception 3"),
            KeyError("exception 4"),
            KeyError("exception 5"),
        ]
    )

    @retry(maxTry=3, wait=1, raise_if_exhausted=False)
    def some_function(*args, **kwargs):
        return my_listener(*args, **kwargs)

    output = some_function("a", "b", c="c")

    assert output is None, "Expect no exception raised and None output since `raise_if_exhausted=False`."
    assert my_listener.call_count == 3, "Expect 3 retries only, since `maxTry=3`."
    assert my_listener.mock_calls == [mock.call("a", "b", c="c")] * 3, "Expect to pass args and kwargs the same way as the function was called."
    assert time.sleep.mock_calls == [mock.call(1), mock.call(1)], "Expect sleep time be 1 since `wait=1`: attempt 1, SLEEP, attempt 2, SLEEP, attempt 3."
    expected_messages = """
attempting calling `some_function`
encountered error calling `some_function`: KeyError('exception 1',)
waiting 1.00s before retrying `some_function`
attempting calling `some_function`
encountered error calling `some_function`: KeyError('exception 2',)
waiting 1.00s before retrying `some_function`
attempting calling `some_function`
encountered error calling `some_function`: KeyError('exception 3',)
"""
    actual_messages = "\n".join([r.message for r in caplog.records])
    assert actual_messages.strip() == expected_messages.strip()


# TODO: implement a default return item, so one can return other values instead of None.


def test_retry_exhaustion_raise_it(monkeypatch, caplog):
    expected_messages = """
attempting calling `some_function`
encountered error calling `some_function`: KeyError('exception 1',)
waiting 3.00s before retrying `some_function`
attempting calling `some_function`
encountered error calling `some_function`: KeyError('exception 2',)
waiting 3.00s before retrying `some_function`
attempting calling `some_function`
encountered error calling `some_function`: KeyError('exception 3',)
"""  # Perhaps more readable to just inspect the log messages; also put at top of test so its known

    caplog.set_level("DEBUG", logger=LOGGER.name)
    monkeypatch.setattr(time, "sleep", mock.Mock())

    my_listener = mock.Mock(
        side_effect=[
            KeyError("exception 1"),
            KeyError("exception 2"),
            KeyError("exception 3"),
            KeyError("exception 4"),
            KeyError("exception 5"),
        ]
    )

    @retry(maxTry=3, wait=3, retryErrs=(KeyError,))  # Default is `raise_if_exhausted=True`
    def some_function(*args, **kwargs):
        return my_listener(*args, **kwargs)

    with pytest.raises(KeyError, match="exception 3"):
        some_function("a", "b", "c")

    actual_messages = "\n".join([r.message for r in caplog.records])
    assert actual_messages.strip() == expected_messages.strip()


def test_retry_successful(monkeypatch, caplog):
    # Retries set to 10, but only 4 should happen because "it-works" is 4th returned item
    expected_messages = """
attempting calling `some_function`
encountered error calling `some_function`: ValueError('exception 1',)
waiting 0.00s before retrying `some_function`
attempting calling `some_function`
encountered error calling `some_function`: ValueError('exception 2',)
waiting 0.00s before retrying `some_function`
attempting calling `some_function`
encountered error calling `some_function`: ValueError('exception 3',)
waiting 0.00s before retrying `some_function`
attempting calling `some_function`
success calling `some_function`
"""

    caplog.set_level("DEBUG", logger=LOGGER.name)
    monkeypatch.setattr(time, "sleep", mock.Mock())

    my_listener = mock.Mock(
        side_effect=[
            ValueError("exception 1"),
            ValueError("exception 2"),
            ValueError("exception 3"),
            "it-works",
        ]
    )

    @retry(maxTry=10, wait=0)
    def some_function(*args, **kwargs):
        return my_listener(*args, **kwargs)

    output = some_function("a", "b", "c")

    assert output == "it-works"

    actual_messages = "\n".join([r.message for r in caplog.records])
    assert actual_messages.strip() == expected_messages.strip()


def test_retry_non_retryable(monkeypatch, caplog):
    # Retries set to 10, but only 3 should happen because 3rd time exception is not retry-able
    expected_messages = """
attempting calling `some_function`
encountered error calling `some_function`: KeyError('exception 1',)
waiting 0.00s before retrying `some_function`
attempting calling `some_function`
encountered error calling `some_function`: ValueError('exception 2',)
waiting 0.00s before retrying `some_function`
attempting calling `some_function`
"""

    caplog.set_level("DEBUG", logger=LOGGER.name)
    monkeypatch.setattr(time, "sleep", mock.Mock())

    my_listener = mock.Mock(
        side_effect=[
            KeyError("exception 1"),
            ValueError("exception 2"),
            TypeError("exception 3"),
            "it-works",
        ]
    )

    @retry(maxTry=10, retryErrs=(KeyError, ValueError), wait=0)
    def some_function(*args, **kwargs):
        return my_listener(*args, **kwargs)

    with pytest.raises(TypeError, match="exception 3"):
        some_function("a", "b", "c")

    actual_messages = "\n".join([r.message for r in caplog.records])
    assert actual_messages.strip() == expected_messages.strip()


# TODO: implement showing the uncaught exception message in the retry log.


def test_retry_err_test(monkeypatch, caplog):
    # Retries set to 10, but only 3 should happen because 3rd time exception is not retry-able (errno != 1)
    expected_messages = """
attempting calling `some_function`
encountered error calling `some_function`: PermissionError(1, 'exception 1')
waiting 3.00s before retrying `some_function`
attempting calling `some_function`
encountered error calling `some_function`: PermissionError(1, 'exception 2')
waiting 3.00s before retrying `some_function`
attempting calling `some_function`
encountered error calling `some_function`: ProcessLookupError(3, 'exception 3')
"""

    caplog.set_level("DEBUG", logger=LOGGER.name)
    monkeypatch.setattr(time, "sleep", mock.Mock())

    my_listener = mock.Mock(
        side_effect=[
            IOError(1, "exception 1"),
            IOError(1, "exception 2"),
            IOError(3, "exception 3"),  # Not retryable per our retryErrTest!
            IOError(1, "exception 3"),
            "it-works",
        ]
    )

    @retry(maxTry=10, retryErrs=(IOError,), retryErrTest=lambda e: e.errno == 1)
    def some_function(*args, **kwargs):
        return my_listener(*args, **kwargs)

    with pytest.raises(IOError, match="exception 3"):
        some_function("a", "b", "c")

    actual_messages = "\n".join([r.message for r in caplog.records])
    assert actual_messages.strip() == expected_messages.strip()


def test_retry_backoff(monkeypatch):
    # Retries set to 10, but only 3 should happen because 3rd time exception is not retry-able (errno != 1)
    monkeypatch.setattr(time, "sleep", mock.Mock())
    my_listener = mock.Mock(
        side_effect=[
            TypeError("exception 1"),
            TypeError("exception 2"),
            TypeError("exception 3"),
            TypeError("exception 4"),
            "it-works",
        ]
    )

    @retry(maxTry=10, wait=15, backoff_multipilier=2)
    def some_function(*args, **kwargs):
        return my_listener(*args, **kwargs)

    output = some_function("a", "b", "c")
    assert output == "it-works"
    assert my_listener.call_count == 5
    # expect 2 waits: try 1, wait 15, try 2, wait 30, try 3, wait 60, try 4
    time.sleep.assert_has_calls([mock.call(15), mock.call(30), mock.call(60)])


# TODO: create fixtures for debug logger and mock time.
