# -*- coding: utf-8 -*-

from os.path import join, dirname

from setuptools import setup, find_packages

import lingvo

setup(
        name="sling",
        version=lingvo.__version__,
        packages=find_packages(
                exclude=["*.exemple", "*.exemple.*", "exemple.*",
                         "exemple"]),
        include_package_data=True,
        long_description=open(
                join(dirname(__file__), 'readme.rst')).read(),
        install_requires=["PyQt5", "pyaml"],
        entry_points={
            'console_scripts':
                ['sling = lingvo.run:main']
        }

)
