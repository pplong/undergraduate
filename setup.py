try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Naive',
    'author': 'Wang Ziyuan',
    'url': 'nope',
    'download_url': 'dummy',
    'author_email': 'pplong360@gmail.com',
    'version': '1.0',
    'install_requires': ['nose'],
    'packages': ['Naive'],
    'scripts': [],
    'name': 'Naive'
}

setup(**config)