from common import *

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
        with open(policy, "w+") as file:
            file.write("hello")
        result = runner.invoke(command, ["stop"])
        assert result.exit_code == 0
        assert exists(policy)
    in_isolation_do(task)

def test_restores_sidelined_policy_enforcer():
    def task(runner):
        with open(policy, "w+") as file:
            file.write("hello")
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
