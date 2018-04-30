==========================================================================
ldap-group-acl-helper - Squid external acl ldap group helper
==========================================================================


What is this?
*************
``ldap-group-acl-helper`` provides an executable called ``ext_acl_ldap_group``
for concurrent squid behavior.

Installation
************
*on most UNIX-like systems, you'll probably need to run the following
`install` commands as root or by using sudo*

**from source**

::

  pip install git+http://github.com/verdel/ldap-group-acl-helper

**or**

::

  git clone git://github.com/verdel/ldap-group-acl-helper.git
  cd ldap-group-acl-helper
  python setup.py install

as a result, the ``ext_acl_ldap_group`` executable will be installed into a
system ``bin`` directory

Usage
-----
::

    ext_acl_ldap_group --help
    usage: ext_acl_ldap_group.py [-h] -d BINDDN [-w BINDPASSWD] [-W SECRETFILE] -s
                                 SERVER [-p PORT] [-z] [-c TIMEOUT] [-t TIMELIMIT]
                                 -b BASEDN -f USER_FILTER -g GROUP_FILTER [-k]
                                 [-n]

    Squid external acl ldap group helper

    optional arguments:
      -h, --help            show this help message and exit
      -d BINDDN, --binddn BINDDN
                            DN to bind as to perform searches
      -w BINDPASSWD, --bindpasswd BINDPASSWD
                            password for binddn
      -W SECRETFILE, --secretfile SECRETFILE
                            read password for binddn from file secretfile
      -s SERVER, --server SERVER
                            LDAP server. Can be set multiple instance. Use first
                            active strategy
      -p PORT, --port PORT  LDAP server port (defaults to 389)
      -z, --ssl             SSL encrypt the LDAP connection
      -c TIMEOUT, --timeout TIMEOUT
                            connect timeout (defaults to 10)
      -t TIMELIMIT, --timelimit TIMELIMIT
                            search time limit (defaults to 10)
      -b BASEDN, --basedn BASEDN
                            base dn under where to search for users and groups
      -f USER_FILTER, --user-filter USER_FILTER
                            user search filter pattern. %u = login
      -g GROUP_FILTER, --group-filter GROUP_FILTER
                            group search filter pattern. %u = login. %g = group
      -k, --strip-realm     strip Kerberos realm from usernames
      -n, --strip-domain    strip NT domain from usernames
