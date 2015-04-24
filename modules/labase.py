"""Module contains common classes and functions required by the package."""


from socket import gethostname, getfqdn, gethostbyname
import sys
import os.path


def getcurnames():
    """Get short and full names. Return tuple."""
    name = gethostname()
    return (name, getfqdn(name))


def getcuraddr():
    """Get ipv4 address. Return str."""
    return gethostbyname(getcurnames()[1])


if __name__ == '__main__':
    print("%s executed directly. It's useless" % os.path.basename(sys.argv[0]))
