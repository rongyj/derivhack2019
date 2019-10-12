from setuptools import setup

setup(name='dabl-hello-bot',
      version='1.0',
      description='DABL Hello Bot',
      author='Digital Asset',
      license='Apache2',
      install_requires=['dazl'],
      packages=['bot'],
      include_package_data=True)
