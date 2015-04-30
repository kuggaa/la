"""Module for ALD configuration."""


import sys
import argparse
import os.path
from labase import Service, getcurnames


class ALDConfigure(Service):
    """docstring"""
    macroses = {'{LA_DOMAIN_NAME}':None,
                '{LA_DOMAIN_CONTROLLER}':None}

    def __init__(self):
        super().__init__('ALD')
        args = get_args()
        self.role = args.role
        self.srv = args.srv
        self.cfg.append('/etc/ald/ald.conf')

    def _populate_macroses(self):
        fqdn = getcurnames()[1]
        self.macroses['{LA_DOMAIN_NAME}'] = fqdn[fqdn.find('.'):]
        if self.role == 'd':
            self.macroses['{LA_DOMAIN_CONTROLLER}'] = fqdn
        else:
            self.macroses['{LA_DOMAIN_CONTROLLER}'] = self.srv


def get_args():
    """Get command line arguments. Return argparse.Namespace."""
    desc = "Configure ALD domain controller, file server or client."
    frmt = argparse.RawTextHelpFormatter
    role_help = """The role in ALD domain. Possible values:
        d - domain contrloller
        f - file server
        c - client (The default).
    """
    parser = argparse.ArgumentParser(description=desc,
                                     formatter_class=frmt)
    # The role in ALD domain.
    parser.add_argument('-r', '--role',
                        help=role_help,
                        choices=['d', 'f', 'c'],
                        nargs='?',
                        metavar='role',
                        default='c',
                        dest='role'
                       )
    # ALD server name (domain controller).
    parser.add_argument('-s', '--server',
                        help='ALD server hostname.',
                        metavar='hostname',
                        required=True,
                        dest='srv'
                       )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    # Self test code
    print(getcurnames())
    print()

    # get_args
    myargs = get_args()
    print(type(myargs))
    print('Role:', myargs.role)
    print('Server:', myargs.srv)

    # ALDConfigure
    dom = ALDConfigure()
    print(dom.name)
    print(dom.role)
    print(dom.srv)
    print(dom.cfg)
    print(dom.templates_dir)
    #dom.save_configs(dom.cfg)
    dom._populate_macroses()
    for key in dom.macroses:
        print(key, '--', dom.macroses[key])

