"""Module contains common classes and functions required by the package."""


from socket import gethostname, getfqdn, gethostbyname
import sys
import time
import os.path
import shutil


# The templates for configuration files must be in this directory.
templates_dir = '/usr/local/lib/la/config-templates'


class LABaseError(Exception):
    """Base exception for this module."""
    pass


class Service:
    """Base class. Must be subclassed."""
    configs = []

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

    def save_configs(self):
        """Save configs with '.la-%d%m%Y-%H%M' suffices."""
        for cfg_file in self.configs:
            self._save_cfg(cfg_file)

    def modify_config(self, cfgfile, template, func):
        """Replace cfgfile with template."""
        with open(cfgfile, 'w') as cfg, open(template) as tmpl:
            for line in tmpl:
                cfg.write(func(line))


def getnetworks():
    """Get name, address, etc.. Return dictionary."""
    res = {}
    res['sname'] = gethostname()
    res['fname'] = getfqdn(res['sname'])
    res['ip'] = gethostbyname(res['fname'])
    # Get domain name by slicing fqdn using short name's length.
    res['dom'] = res['fname'][len(res['sname']):]
    return res


if __name__ == '__main__':
    # Self testing code.
    nets = getnetworks()
    for key in nets.keys():
        print(key, '-->', nets[key])
