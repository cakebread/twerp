from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.0.3'

install_requires = ['twilio>=3.3.3', 'ConfigObj', 'clint']


setup(name='twerp',
    version=version,
    description="Twilio command-line application for sending SMS text messages and making voice calls.",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Communications :: Telephony',
        'Topic :: Communications :: Internet Phone',
        'Topic :: Communications :: Conferencing'
    ],
    keywords='twilio sms telephony',
    author='Rob Cakebread',
    author_email='cakebread@gmail.com',
    url='http://github.com/cakebread/twerp',
    license='BSD',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['twerp=twerp.cli:main']
    }
)
