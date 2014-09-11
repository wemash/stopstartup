"""
http://serverfault.com/questions/567474/how-can-i-install-packages-without-starting-their-associated-services
"""
from click import group, echo, pass_context, make_pass_decorator
from collections import namedtuple


State = namedtuple("State", ("home", "install_dir"))
pass_state = make_pass_decorator(State, ensure = True)

@group()
def cli():
    """
    Packages that install a service and then automatically execute it are
    annoying. Why deal with it? Why not just take advantage of the fact that
    LSB compliant packages must use invoke-rc.d to start these services, and
    that invoke-rc.d defers to /usr/sbin/policy-rc.d?


    Calling start will replace the current policy enforcer at
    /usr/sbin/policy-rc.d with a custom one that will reject every request.
    
    Calling stop will remove the custom enforcer, and will put your old
    enforcer back in place, assuming you had one.
    """
    pass

def exists(path):
    """
    Determine if a path is:
    1. a link
    2. a file
    3. a directory
    """
    from os.path import isfile, islink, isdir
    return isfile(path) or islink(path) or isdir(path)

def are_the_same(first, second):
    """
    Determine if two paths point to the same thing.
    Symbolic links will be followed to the very end.
    """
    from os.path import realpath
    return realpath(first) == realpath(second)

@cli.command()
@pass_state
def start(state):
    """
    Start stopping services from starting...

    Any existing policy enforcer will be sidelined. You must call stop to undo
    the sidelining. It is also not recommended that you manually replace the
    installed policy enforcer after calling start and before calling stop;
    doing so may cause your original policy enforcer to be overwritten during
    the sidelining process.
    """
    from os import symlink
    from os.path import join
    from shutil import move
    source = join(state.home, "policy-rc.d")
    destination = join(state.install_dir, "policy-rc.d")
    sideline = join(state.install_dir, "policy-rc.d.sidelined")
    if are_the_same(source, destination):
        echo("Stopping has already been started!")
        return
    if exists(destination):
        echo("A policy enforcer existed, and was sidelined")
        move(destination, sideline)
    symlink(source, destination)
    

@cli.command()
@pass_state
def stop(state):
    """Stop stopping services from starting..."""
    from os.path import join
    from os import remove
    from shutil import move
    original = join(state.home, "policy-rc.d")
    policy = join(state.install_dir, "policy-rc.d")
    sideline = join(state.install_dir, "policy-rc.d.sidelined")
    if not exists(policy):
        echo("Negative policy enforcement has already stopped!")
        return
    if not are_the_same(original, policy):
        return
    if exists(policy):
        remove(policy)
    if exists(sideline):
        move(sideline, policy)

if __name__ == "__main__":
    cli()
