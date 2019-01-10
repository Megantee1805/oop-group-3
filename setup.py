import io

from setuptools import find_packages, setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='foodhubsg',
    version='1.0.0',
    license='BSD',
    maintainer='OOPP Group 3',
    maintainer_email='bala12rupesh@gmail.com',
    description='A health app that recommends healthy food near you',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)
