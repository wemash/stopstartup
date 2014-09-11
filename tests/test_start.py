from common import *
from os import symlink, access, X_OK as EXECUTABLE

def test_creates_policy_enforcer():
    def task(runner):
        result = runner.invoke(command, ["start"])
        assert result.exit_code == 0
        assert exists(policy)
    in_isolation_do(task)


def test_sidelines_existing_policy_enforcers_to_the_side():
    def try_to_sideline(some_candidate_generator):
        def task(runner):
            some_candidate_generator()
            result = runner.invoke(command, ["start"])
            assert result.exit_code == 0
            assert exists(sidelined)
            assert result.output == "A policy enforcer existed, and was sidelined\n"
        in_isolation_do(task)

    def file_candidate():
        with open(policy, "w+") as file:
            file.write("hello")

    def link_candidate():
        with open("asdf", "w+") as file:
            file.write("policy-rc.d")
        symlink("policy-rc.d", policy)

    try_to_sideline(file_candidate)
    try_to_sideline(link_candidate)

def test_doesnt_sideline_self():
    def task(runner):
        runner.invoke(command, ["start"])
        result = runner.invoke(command, ["start"])
        assert not exists(sidelined)
        assert result.output == "Stopping has already been started!\n"
    in_isolation_do(task)

def test_is_executable():
    def task(runner):
        runner.invoke(command, ["start"])
        assert access(policy, EXECUTABLE)
    in_isolation_do(task)
