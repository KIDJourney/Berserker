from setuptools import setup, find_packages
from berserker import version

install_requires = ['gevent', 'requests>=2.3.0']

description = 'Web Application Smoking Test'

classifiers = ["License :: OSI Approved :: MIT License",
               "Programming Language :: Python :: 3.3",
               "Programming Language :: Python :: 3.4",
               "Programming Language :: Python :: 3.5",
               "Programming Language :: Python :: 3.6"]

setup(name='berserker',
      version=version,
      url='https://github.com/KIDJourney/Berserker',
      packages=find_packages(),
      long_description=description,
      author="KIDJourney",
      author_email="kingdeadfish@qq.com",
      classifiers=classifiers,
      install_requires=install_requires,
      entry_points="""
      [console_scripts]
      berserker = berserker.core:main
      """)
