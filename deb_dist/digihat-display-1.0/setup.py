import os
import io
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(name              = 'Digihat_display',
      version           = '1.0',
      author            = 'Ben Payne, Yash Gandhi',
      author_email      = 'yash@bluerocksoft.com',
      description       = 'python code for digital hat display',
      long_description  = long_description,
      license           = 'MIT',
      classifiers       = classifiers,
      url               = 'https://github.com/InterludeAudio/digihat_display',
      packages          = find_packages(),
      entry_points={
        'console_scripts': [
            'display.py = Digihat_display.module:main',
        ]
    }
)
