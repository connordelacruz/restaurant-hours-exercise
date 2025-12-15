from setuptools import setup, find_packages

setup(
    name='restaurant_hours',
    version='0.0.1',
    author='Connor de la Cruz',
    author_email='connor.c.delacruz@gmail.com',
    description='API to check open restaurants given a date/time.',
    packages=find_packages(),
    install_requires=[
        'Flask>=3.1,<3.2',
        'Flask-RESTful>=0.3,<0.4',
    ],
)