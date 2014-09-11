from common import *
from os import chmod

def test_removes_policy_enforcer():
    def task(runner):
        runner.invoke(command, ["start"])
        result = runner.invoke(command, ["stop"])
        assert result.exit_code == 0
        assert not exists(policy)
        assert not exists(sidelined)
    in_isolation_do(task)

def test_doesnt_remove_policy_enforcer_if_not_self():
    def task(runner):
        touch(policy)
        result = runner.invoke(command, ["stop"])
        assert result.exit_code == 1
        assert exists(policy)
    in_isolation_do(task)

def test_restores_sidelined_policy_enforcer():
    def task(runner):
        touch(policy)
        runner.invoke(command, ["start"])
        result = runner.invoke(command, ["stop"])
        assert result.exit_code == 0
        assert not exists(sidelined)
        assert exists(policy)
        assert open(policy).read() == "hello"
    in_isolation_do(task)

def test_can_be_called_multiple_times():
    def task(runner):
        runner.invoke(command, ["stop"])
        runner.invoke(command, ["stop"])
        result = runner.invoke(command, ["stop"])
        assert result.exit_code == 0
        assert result.output == "Negative policy enforcement has already stopped!\n"
    in_isolation_do(task)

def test_panics_if_status_is_broken():
    def task(runner):
        touch(policy)
        touch(sidelined)
        result = runner.invoke(command, ["stop"])
        assert result.exit_code == 1
        assert matches(result.output, "BROKEN")
    in_isolation_do(task)

def test_gracefully_handles_lack_of_permission():
    def task(runner):
        runner.invoke(command, ["start"])
        chmod(root, 0555)
        result = runner.invoke(command, ["stop"])
        assert result.exit_code == 1
        assert matches(result.output, "ELEVATE ME")
    in_isolation_do(task)
