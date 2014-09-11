Stop most services from starting
================================

Some Debian package installs automatically launch an instance, and sometimes
you don't want that to happen immediately. :code:`stopstartup`, when activated,
will stop any service started via :code:`invoke-rc.d` from starting. It does
this by hijacking :code:`/usr/sbin/policy-rc.d`, which :code:`invoke-rc.d`
calls for every service.  Normally the file should determine if your currently
active "policy" (whatever that means) should allow the service to startup. The
policy enforcer installed by :code:`stopstartup` is much less nice, and simply
rejects any request.

The policy is installed at :code:`usr/sbin/`, so if you don't have proper
permissions there you'll be unable to run :code:`stopstartup`. If that happens,
try using :code:`sudo`.
