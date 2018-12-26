import io

from setuptools import find_packages, setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='api',
    version='0.2.0',
    license='MIT',
    maintainer='Luke Smith',
    maintainer_email='lsmith@zenoscave.com',
    description='Flask API for dotProj ',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'docker',
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
        ],
    },
)