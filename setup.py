from distutils.core import setup

setup(name = "la",
      version = "0.1",
      description = "Configure the services of Astra Linux SE.",
      author = "Vladimir Golubkov",
      author_email = "support@rusbitech.ru",
      url = "http://astra-linux.com",
      packages = ['la'],
      package_dir = {'la': 'modules'},
      scripts = ['la-run'],
      long_description = """long description"""
     )
