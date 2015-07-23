"""Module contains common classes and functions required by the package."""


from socket import gethostname, getfqdn, gethostbyname
import sys
import time
import os.path
import shutil


class Service:
    """Base class. Must be subclassed."""
    cfg = []
    # The templates for configuration files must be in this directory.
    templates_dir = '/usr/local/lib/config-templates'

    def __init__(self, name):
        self.name = name

    def __str__(self):
        res = []
        res.append('Class: %s\nAttributes:' % self.__class__)
        for key in self.__dict__.keys():
            res.append(str(key) + ' --> ' + str(self.__dict__[key]))
        return '\n'.join(res)

    def _save_cfg(self, cfgfile):
        suffix = time.strftime('.la-%d%m%Y-%H%M', time.localtime())
        shutil.copy(cfgfile, cfgfile + suffix)

    def save_configs(self, cfg):
        """Save configs with '.la-%d%m%Y-%H%M' suffices."""
        for cfg_file in cfg:
            self._save_cfg(cfg_file)

    def modify_config(self, cfgfile, template, func):
        """Replace cfgfile with template."""
        with open(cfgfile, 'w') as cfg, open(template) as tmpl:
            for line in tmpl:
                cfg.write(func(line))


def getcurnames():
    """Get short and full names. Return tuple."""
    name = gethostname()
    return (name, getfqdn(name))


def getcuraddr():
    """Get ipv4 address. Return str."""
    return gethostbyname(getcurnames()[1])


if __name__ == '__main__':
    print("%s executed directly. It's useless" % os.path.basename(sys.argv[0]))
