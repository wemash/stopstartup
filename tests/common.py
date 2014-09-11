from stopstartup import State, start, stop, status, exists
from click import group, pass_context
from click.testing import CliRunner
from os.path import join
from os import getcwd, makedirs
from re import compile


home = getcwd()
root = join("usr", "sbin")
policy = join(root, "policy-rc.d")
sidelined = join(root, "policy-rc.d.sidelined")

@group()
@pass_context
def command(context):
    context.obj = State(home, root)
command.add_command(start)
command.add_command(stop)
command.add_command(status)

def in_isolation_do(task):
    runner = CliRunner()
    with runner.isolated_filesystem():
        makedirs(root)
        task(runner)

def matches(source, pattern):
    return compile(pattern).match(source)

def touch(path):
    with open(path, "w+") as file:
        file.write("hello")
