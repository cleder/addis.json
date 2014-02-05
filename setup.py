from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='addis.json',
      version=version,
      description="",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='UNEP ADDIS Json API',
      author='Christian Ledermann',
      author_email='christian.ledermann@gmail.com',
      url='https://github.com/cleder/addis.json',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['addis'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'simplejson',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      #setup_requires=["PasteScript"],
      #paster_plugins=["ZopeSkel"],
      )
