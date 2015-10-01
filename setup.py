from distutils.core import setup
import os.path


# ct - config template
ct_src = 'modules/config-templates'
ct_dest = 'lib/la/config-templates'

setup(name="la",
      version="0.1.0",
      description="Configure Astra Linux SE services.",
      author="Vladimir Golubkov",
      author_email="vgol.mail@gmail.com",
      url="http://astra-linux.com",
      packages=["la"],
      package_dir={"la": "modules"},
      scripts=["la-run"],
      data_files=[(ct_dest, [os.path.join(ct_src, "ald.conf")])],
      # TODO: Write proper long description.
      long_description="""Configure Astra Linux SE services."""
      )
