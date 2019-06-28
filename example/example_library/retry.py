import logging
import time

LOGGER = logging.getLogger(__name__)

WINDOWS = "win"
LINUX = "linux"


returnTrue = lambda x: True


def retry(
    maxTry,
    retryErrs=(),
    failErrs=(),
    retryErrTest=returnTrue,
    wait=3,
    raise_if_exhausted=True,
    backoff_multipilier=1,
):
    """
    A decorator to retry a function, in the case of an exception.

    Give only either retryErrs OR failErrs, not both.
        -   failErrs: retry everything BUT these exceptions.
        -   retryErrs: retry only the specified exceptions.

    @param maxTry: the number of times to retry the decorated function
    @param retryErrs: this should be a tuple of Exception types
    @param failErrs: this can be an exception type or tuple of exception types
    @param retryErrTest: a function that will return True if the error instance should be retried
    Note: you can use this argument to trigger a side effect like a reconnect.
    @param wait: time (seconds) to wait before retrying (default=3)
    @param raise_if_exhausted: Raise the last error.
    @param backoff_multipilier: multiplier to multiply wait time.
    @return: decorated function
    """
    # This exception will never get raised from the outside, used as "no fail errors"
    class _PrivateException(Exception):
        pass

    _fail_errors = failErrs or _PrivateException

    if failErrs:
        _retryErrs = (Exception,) + retryErrs
    elif not retryErrs:
        _retryErrs = Exception
    else:
        _retryErrs = retryErrs

    def runFunction(origFunction):
        fn_name = origFunction.__name__

        def f(*args, **kwargs):
            attempts = 0
            except_inst = None
            local_wait = wait
            while (attempts < maxTry) and (except_inst is None or retryErrTest(except_inst)):
                try:
                    attempts += 1
                    if attempts != 1:
                        LOGGER.info(
                            "waiting {:.2f}s before retrying `{}`".format(local_wait, fn_name)
                        )
                        time.sleep(local_wait)
                        local_wait *= backoff_multipilier
                    LOGGER.debug("attempting calling `{}`".format(fn_name))
                    result = origFunction(*args, **kwargs)
                    LOGGER.debug("success calling `{}`".format(fn_name))
                    return result
                except _fail_errors:
                    raise
                except _retryErrs as e:
                    except_inst = e
                    LOGGER.warning("encountered error calling `{}`: {!r}".format(fn_name, e))
                    pass
            if raise_if_exhausted and except_inst:
                raise except_inst

        return f

    return runFunction
