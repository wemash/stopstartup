from common import *


def test_knows_when_policy_enforcement_is_inactive():
    def task(runner):
        result = runner.invoke(command, ["status"])
        assert result.exit_code == 0
        assert matches(result.output, "INACTIVE")
    in_isolation_do(task)

def test_knows_when_policy_enforcement_is_active():
    def task(runner):
        runner.invoke(command, ["start"])
        result = runner.invoke(command, ["status"])
        assert result.exit_code == 0
        assert matches(result.output, "ACTIVE")
    in_isolation_do(task)

def test_knows_when_third_party_policy_enforcement_is_active():
    def task(runner):
        touch(policy)
        result = runner.invoke(command, ["status"])
        assert result.exit_code == 0
        assert matches(result.output, "INACTIVE")
    in_isolation_do(task)

def test_knows_when_policy_enforcement_is_broken():
    def orphaned_sideline(runner):
        touch(sidelined)
        result = runner.invoke(command, ["status"])
        assert result.exit_code == 1
        assert matches(result.output, "BROKEN!")

    def sideline_plus_third_party_enforcer(runner):
        touch(policy)
        touch(sidelined)
        result = runner.invoke(command, ["status"])
        assert result.exit_code == 1
        assert matches(result.output, "BROKEN!")
    in_isolation_do(orphaned_sideline)
    in_isolation_do(sideline_plus_third_party_enforcer)
