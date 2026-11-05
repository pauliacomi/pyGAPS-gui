import logging

import pytest

from pygapsgui.utilities.log_hook import LogHook
from pygapsgui.utilities.log_hook import calculation_error
from pygapsgui.utilities.log_hook import log_hook


def test_log_hook_propagates_and_removes_handlers():
    hook = LogHook()
    handlers = list(hook.logger.handlers)
    with pytest.raises(TypeError, match="unexpected"):
        with hook:
            raise TypeError("unexpected")
    assert hook.logger.handlers == handlers


def test_logs_are_escaped_and_use_inherited_info_colour(caplog):
    caplog.set_level(logging.INFO, logger="pygaps")
    hook = LogHook()
    with hook:
        hook.logger.info("p < 0.05 & p > 0")
        hook.logger.warning("warning <tag>")
        hook.logger.log(logging.CRITICAL, "critical")
    logs = hook.get_logs()
    assert "p &lt; 0.05 &amp; p &gt; 0" in logs
    assert 'color="black"' not in logs
    assert "warning &lt;tag&gt;" in logs
    assert "critical" in logs
    assert hook.get_logs() == ""


def test_failed_calculation_drains_logs():
    with log_hook:
        log_hook.logger.warning("first calculation")
        output = calculation_error(ValueError("<invalid>"))
    assert "first calculation" in output
    assert "&lt;invalid&gt;" in output
    with log_hook:
        log_hook.logger.info("second calculation")
    assert "first calculation" not in log_hook.get_logs()
