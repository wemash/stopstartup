from stopstartup import State, start, exists
from os import makedirs, symlink, getcwd, access, X_OK as EXECUTABLE
from os.path import join
from click import group, pass_context
from click.testing import CliRunner


home = getcwd()
root = join("usr", "sbin")
policy = join(root, "policy-rc.d")
sidelined = join(root, "policy-rc.d.sidelined")

@group()
@pass_context
def startup(context):
    context.obj = State(home, root)
startup.add_command(start)

def in_isolation_do(task):
    runner = CliRunner()
    with runner.isolated_filesystem():
        makedirs(root)
        task(runner)

def test_creates_policy_enforcer():
    def task(runner):
        result = runner.invoke(startup, ["start"])
        assert result.exit_code == 0
        assert exists(policy)
    in_isolation_do(task)


def test_sidelines_existing_policy_enforcers_to_the_side():
    def try_to_sideline(some_candidate_generator):
        def task(runner):
            some_candidate_generator()
            result = runner.invoke(startup, ["start"])
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
        runner.invoke(startup, ["start"])
        result = runner.invoke(startup, ["start"])
        assert not exists(sidelined)
        assert result.output == "Stopping has already been started!\n"
    in_isolation_do(task)

def test_is_executable():
    def task(runner):
        runner.invoke(startup, ["start"])
        assert access(policy, EXECUTABLE)
    in_isolation_do(task)
