from setuptools import setup, find_packages

setup(
    version='0.10',
    author='Erik Woidt',
    author_email='erik@woidt.be',
    packages=find_packages(exclude='test'),
    name='Storage',
    install_requires=['pika', 'jsonschema', 'SQLAlchemy==1.3.0b1', 'mysqlclient', 'click'],
    include_package_data=True,
    url='',
    entry_points={
        'console_scripts': [
            'main = storage:main',
        ]
    }
)