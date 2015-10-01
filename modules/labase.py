"""Module contains common classes and functions required by the package."""


from socket import gethostname, getfqdn, gethostbyname
import time
import shutil


# The templates for configuration files must be in this directory.
templates_dir = "/usr/local/lib/la/config-templates"


class LABaseError(Exception):
    """Base exception for this module."""
    pass


class Service:
    """Base class. Must be subclassed."""
    configs = []

    def __init__(self, name):
        self.name = name

    def __str__(self):
        res = ["Class: %s\nAttributes:" % self.__class__]
        for k in self.__dict__.keys():
            res.append("{0} --> {1}".format(str(k), str(self.__dict__[k])))
        return '\n'.join(res)

    @staticmethod
    def _save_cfg(configfile):
        suffix = time.strftime(".la-%d%m%Y-%H%M", time.localtime())
        shutil.copy(configfile, configfile + suffix)

    def save_configs(self):
        """Save configs with '.la-%d%m%Y-%H%M' suffices."""
        for cfg_file in self.configs:
            self._save_cfg(cfg_file)

    @staticmethod
    def modify_config(configfile, template, func):
        """Replace configfile with template."""
        with open(configfile, 'w') as cfg, open(template) as tmpl:
            for line in tmpl:
                cfg.write(func(line))


def getnetworks():
    """Get name, address, etc.. Return dictionary."""
    res = {"sname": gethostname()}
    res["fname"] = getfqdn(res["sname"])
    res["ip"] = gethostbyname(res["fname"])
    # Get domain name by slicing fqdn using short name's length.
    res["dom"] = res["fname"][len(res["sname"]):]
    return res


if __name__ == "__main__":
    # Self testing code.
    nets = getnetworks()
    for key in nets.keys():
        print("{0} --> {1}".format(key, nets[key]))
