from stopstartup import State, start, stop, exists
from click import group, pass_context
from click.testing import CliRunner
from os.path import join
from os import getcwd, makedirs


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

def in_isolation_do(task):
    runner = CliRunner()
    with runner.isolated_filesystem():
        makedirs(root)
        task(runner)
