"""Module for ALD configuration."""


import sys
import labase


# Macroses
# {LA_DOMAIN_NAME}
# {LA_DOMAIN_CONTROLLER}

# Required arguments:
# - type: controller, fs, of client
# - controller name: hostname


class ALDConfigure(type, dc):
    """docstring"""
    def __init__(self, type, dc)
        self.type = type
        self.dc = dc


def usage():
    """Usage text."""
    print(usage.__doc__)


def args():

def usage():
    """Usage text."""
    print(usage.__doc__)


if __name__ == '__main__':
    # Self test code
    print('%s executed directly' % sys.argv[0])
    print(labase.getcurnames())
    print(labase.getcuraddr())
