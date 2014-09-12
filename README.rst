Stop most services from starting
================================

Some Debian package installs automatically launch a daemon, and sometimes you
don't want that to happen immediately. :code:`stopstartup`, when activated,
will stop any service started via :code:`invoke-rc.d` from starting. It does
this by hijacking :code:`/usr/sbin/policy-rc.d`, which :code:`invoke-rc.d`
calls for every service.  Normally the file should determine if your currently
active "policy" (whatever that means) should allow the service to startup. The
policy enforcer installed by :code:`stopstartup` is much less nice, and simply
rejects any request.

The policy is installed at :code:`usr/sbin/`, so if you don't have proper
permissions there you'll be unable to run :code:`stopstartup`. If that happens,
try using :code:`sudo`.

Installing
----------

:code:`stopstartup` can be installed in these ways::

    # Install right from Github
    pip install git+https://github.com/wemash/stopstartup

    # Install from a local copy of the repo
    # This is super handy if you want to work on stopstartup
    git clone https://github.com/wemash/stopstartup
    cd stopstartup
    pip install --editable .

    # RECOMMENDED: Install through pip
    pip install stopstartup

Ensuring that this actually works
---------------------------------

A full test suite exists in :code:`tests`. The tests rely on pytest_ and
pytest-pythonpath_. Install those first, then just run :code:`py.test`. The
tests should never create, move, or delete any tests on your real filesystem;
if you write new tests, please use :code:`in_isolation_do` to ensure that your
tests are run in a temporary part of the FS that will be automatically removed
at the completion of the test.

Contributing
------------

Fork this repo and send me a pull request. It's all rather informal.

.. _pytest: https://pytest.org/latest
.. _pytest-pythonpath: https://pypi.python.org/pypi/pytest-pythonpath
