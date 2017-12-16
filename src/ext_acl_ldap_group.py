#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ldap3 import Server, ServerPool, Connection, FIRST, AUTO_BIND_NO_TLS, SUBTREE
import argparse
from os import path
import sys


def get_ldap_connection(server=[], port='', ssl=False, timeout=0, binddn='', bindpasswd=''):
    try:
        server_pool = ServerPool([Server(item, port, use_ssl=ssl) for item in server],
                                 FIRST,
                                 active=3,
                                 exhaust=60)
        conn = Connection(server_pool,
                          auto_bind=AUTO_BIND_NO_TLS,
                          read_only=True,
                          receive_timeout=timeout,
                          check_names=True,
                          user=binddn, password=bindpasswd)
    except Exception as exc:
        print('ext_acl_ldap_group LDAP bind error {}({})'.format(type(exc).__name__, exc))
    else:
        return conn


def get_ldap_info(connection='', timelimit=0, basedn='', username='', user_filter='', group='', group_filter=''):
    if not connection:
        print('BH message="LDAP connection could not be established"')
        return False

    try:
        connection.search(search_base=basedn,
                          search_filter=u'(&({}))'.format(user_filter.replace('%u', username.decode('utf-8'))),
                          search_scope=SUBTREE,
                          time_limit=timelimit,
                          get_operational_attributes=True)

        if len(connection.response) > 0:
            user = connection.response[0]['dn']
            connection.search(search_base=basedn,
                              search_filter=group_filter.replace('%u', user).replace('%g', group.decode('utf-8')),
                              search_scope=SUBTREE,
                              time_limit=timelimit,
                              get_operational_attributes=True)
            if len(connection.response) > 0:
                for item in connection.response:
                    if 'dn' in item:
                        print(u'OK tag="{}"'.format(group.decode('utf-8')))
                        return
                print('ERR')
            else:
                print('ERR')
        else:
            print('ERR')

    except Exception as exc:
        print('BH message={}({})'.format(type(exc).__name__, exc))


def create_cli():
        parser = argparse.ArgumentParser(description='Squid external acl ldap group helper')
        parser.add_argument('-d', '--binddn', type=str, required=True,
                            help='DN to bind as to perform searches')
        parser.add_argument('-w', '--bindpasswd', type=str,
                            help='password for binddn')
        parser.add_argument('-W', '--secretfile',
                            help='read password for binddn from file secretfile')
        parser.add_argument('-s', '--server', action='append', required=True,
                            help='LDAP server. Can be set multiple instance. Use first active strategy')
        parser.add_argument('-p', '--port', type=int, default=389,
                            help='LDAP server port (defaults to %(default)i)')
        parser.add_argument('-z', '--ssl', action='store_true',
                            help='SSL encrypt the LDAP connection')
        parser.add_argument('-c', '--timeout', type=int, default=10,
                            help='connect timeout (defaults to %(default)i)')
        parser.add_argument('-t', '--timelimit', type=int, default=10,
                            help='search time limit (defaults to %(default)i)')
        parser.add_argument('-b', '--basedn', type=str, required=True,
                            help='base dn under where to search for users and groups')
        parser.add_argument('-f', '--user-filter', type=str, required=True,
                            help='user search filter pattern. %%u = login')
        parser.add_argument('-g', '--group-filter', type=str, required=True,
                            help='group search filter pattern. %%u = login. %%g = group')
        parser.add_argument('-k', '--strip-realm', action='store_true',
                            help='strip Kerberos realm from usernames')
        parser.add_argument('-n', '--strip-domain', action='store_true',
                            help='strip NT domain from usernames')
        return parser


def main():
    parser = create_cli()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    conn = None

    if hasattr(args, 'bindpasswd') and args.bindpasswd:
        bindpasswd = args.bindpasswd
    elif hasattr(args, 'secretfile') and args.secretfile:
        if path.isfile(args.secretfile):
            try:
                with open(args.secretfile, 'r') as passwdfile:
                    bindpasswd = passwdfile.readline().replace('\n', '')
            except Exception as exc:
                print('ext_acl_ldap_group Runtime error {}({})'.format(type(exc).__name__, exc))
                bindpasswd = ''
        else:
            print('ext_acl_ldap_group Password file {} not found'.format(args.secretfile))
            bindpasswd = ''
    else:
        print('ext_acl_ldap_group Password for binddn is not set')
        bindpasswd = ''

    if bindpasswd:
        try:
            conn = get_ldap_connection(server=args.server,
                                       port=args.port,
                                       ssl=args.ssl,
                                       timeout=int(args.timeout),
                                       binddn=args.binddn,
                                       bindpasswd=bindpasswd)
        except:
            pass

    while 1:
        try:
            input = sys.stdin.readline()
            if len(input) == 0:
                raise RuntimeError
            else:
                input = input.split()
        except:
            if isinstance(conn, Connection):
                if conn.bound:
                    conn.unbind()
            sys.exit()

        try:
            username = input[0]
            group = input[1]

            if args.strip_realm:
                username = username.split('@')[0]
            if args.strip_domain and '\\' in username:
                username = username.split('\\')[1]

            if isinstance(conn, Connection):
                if conn.closed:
                    conn = get_ldap_connection(server=args.server,
                                               port=args.port,
                                               tls=args.tls,
                                               timeout=int(args.timeout),
                                               binddn=args.binddn,
                                               bindpasswd=bindpasswd)
                if conn.bound:
                    get_ldap_info(connection=conn,
                                  timelimit=int(args.timelimit),
                                  basedn=args.basedn,
                                  username=username,
                                  user_filter=args.user_filter,
                                  group=group,
                                  group_filter=args.group_filter)

            else:
                print('BH message="LDAP connection could not be established"')

            sys.stdout.flush()
        except:
            continue


if __name__ == '__main__':
    main()
