"""Module for ALD configuration."""


import sys
import argparse
import os.path
import textwrap
from labase import Service, getnetworks, templates_dir


class ALDConfigError(Exception):
    """Base exception of this module."""
    pass


class ALDConfig(Service):
    """docstring"""

    def __init__(self):
        super().__init__('ALD')
        self.configs.append('/etc/ald/ald.conf')
        self.role = ''
        self.srv = ''
        self.passwd = ''

    def get_args(self):
        """Get command line arguments and set class parameters."""
        desc = textwrap.dedent("""\
                  ALD configuration tool. You need to specify
                admin's password, server's hostname and
                the role of the current computer in ALD domain
                in options (see below).
                """)
        frmt = argparse.RawTextHelpFormatter
        parser = argparse.ArgumentParser(description=desc,
                                         formatter_class=frmt)
        # The role in ALD.
        role_help = textwrap.dedent("""\
                        the role in ALD. Possible values:
                            d - domain contrloller
                            f - file server
                            c - client (default)
                        """)
        parser.add_argument('-r', '--role',
                            help=role_help,
                            choices=['d', 'f', 'c'],
                            nargs='?',
                            metavar='ROLE',
                            default='c',
                            dest='role'
                           )
        # ALD server name (domain controller).
        parser.add_argument('-s', '--server',
                            help='ALD server hostname.',
                            metavar='SERVER_HOSTNAME',
                            required=True,
                            dest='srv'
                           )
        # Admin password (for now it's the same for K/M and admin/admin).
        passwd_help = textwrap.fill("ALD admin password.")
        parser.add_argument('-p', '--password',
                            help=passwd_help,
                            metavar='PASSWORD',
                            required=True,
                            dest='passwd'
                           )
        args = parser.parse_args()
        self.role = args.role
        self.srv = args.srv
        self.passwd = args.passwd

    def ald_conf_edit(self, line):
        """Replace markers with values. Return str."""
        # shortcuts for markers
        mdom = '{LA_DOMAIN_NAME}'
        mserv = '{LA_DOMAIN_CONTROLLER}'

        if mdom in line:
            res_line = line.replace(mdom, getnetworks()['dom'])
        elif mserv in line:
            res_line = line.replace(mserv, self.srv)
        else:
            res_line = line
        return res_line

    def ald_init(self):
        """Initialize domain controller."""
        pass

    def ald_join(self):
        """Join ALD-client to the domain."""
        pass

    def ald_filesrv_init(self):
        """Initialize file server."""


if __name__ == '__main__':
    # Self test code
    ald = ALDConfig()
    print("Just created an instance of ALDConfig")
    print(ald)
    ald.get_args()
    print("And now we got an arguments")
    print(ald)
    print("Save configs")
    ald.save_configs()
    print("Modify ald.conf")
    ald.modify_config('/etc/ald/ald.conf',
                      os.path.join(templates_dir, 'ald.conf'),
                      ald.ald_conf_edit)
