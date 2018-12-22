import io

from setuptools import find_packages, setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='dotProj_builder',
    version='0.2.0',
    license='MIT',
    maintainer='Luke Smith',
    maintainer_email='lsmith@zenoscave.com',
    description='Build engine for dotProj',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov',
        ],
    },
    entry_points={
        'console_scripts': ['dotproj_build=builder.__main__:main']
    }
)