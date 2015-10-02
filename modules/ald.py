"""Module for ALD configuration."""

import argparse
import os.path
import textwrap
import sys
import subprocess

try:
    # noinspection PyUnresolvedReferences
    from labase import Service, getnetworks, templates_dir
except ImportError:
    print("You need to execute 'setup.py install' first!")
    sys.exit("installation required")


class ALDConfigError(Exception):
    """Base exception of this module."""
    pass


class ALDConfig(Service):
    """TODO: implement the docstring"""

    def __init__(self):
        super().__init__("ALD")
        self.configs.append("/etc/ald/ald.conf")
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
                            d - domain controller
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

    def _create_passwdfile(self):
        """Create password file. Save path in self.passwdfile."""
        assert self.passwd, "password is not given"
        self.passwdfile = os.path.join(os.getenv('HOME'), 'ald-passwd')
        with open(self.passwdfile, 'w') as pf:
            pf.write("admin/admin:{0}\nK/M:{0}".format(self.passwd))
        # Set stricter permissions: only owner can read password file.
        os.chmod(self.passwdfile, 0o400)

    def _remove_passwdfile(self):
        """Remove file from path self.passwdfile"""
        os.unlink(self.passwdfile)

    def ald_exec(self, cmd, *args):
        """Create passwd file. Then execute cmd(*args). Then remove passwd."""
        self._create_passwdfile()
        try:
            cmd(*args)
        finally:
            self._remove_passwdfile()

    @staticmethod
    def init(passwd):
        """Initialize domain controller. Returncode - int."""
        retval = subprocess.check_call(['/usr/sbin/ald-init',
                                        'init',
                                        '--force',
                                        '--pass-file={}'.format(passwd)]
                                       )
        return retval

    @staticmethod
    def join(passwd, server):
        """Join ALD client to the domain."""
        retval = subprocess.check_call(['/usr/sbin/ald-client',
                                        'join',
                                        server,
                                        '--force',
                                        '--pass-file={}'.format(passwd)]
                                       )
        return retval

    @staticmethod
    def filesrv(passwd, server):
        """Join ALD client. Then initialize file server."""
        ALDConfig.join(passwd, server)
        retval = subprocess.check_call(['/usr/sbin/ald-client',
                                        'filesrv-init',
                                        '--force',
                                        '--pass-file={}'.format(passwd)]
                                       )
        return retval


# TODO: Make convenient functions for configure various ALD roles.


if __name__ == '__main__':
    ald = ALDConfig()
    ald.get_args()
    ald.save_configs()

    if ald.role == 'd':
        ald.modify_config(ald.configs[0],
                          os.path.join(templates_dir, 'ald.conf'),
                          ald.ald_conf_edit
                          )
        # FIXME: Something wrong with this statement.
        # ald.ald_exec(ald.init(ald.passwdfile))
    elif ald.role == 'f':
        ald.alc_exec(ald.filesrv(ald.passwdfile, ald.srv))
    else:
        ald.ald_exec(ald.join(ald.passwdfile, ald.srv))
