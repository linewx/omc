from setuptools import setup, find_packages
install_requires = [
    'requests==2.22.0',
    'dynaconf[all]==2.2.3',
    'pyfiglet==0.8.post1',
    'Click==7.0',
    'psutil',
    'kubernetes==11.0.0',
    'ruamel-yaml==0.15.46',
    'prettytable==0.7.2'
]


setup(
    name='omt',
    version=0.01,
    description='oh my tools',
    license='MIT',
    author='Lu Ganlin',
    author_email='gan-lin.lu@microfocus.com',
    url='https://github.houston.softwaregrp.net/Gan-Lin-Lu/omt',
    packages=find_packages(),
    package_data={'omt.config': ['*.yaml'], 'omt.lib': ['**', '**/*', '**/**/*']},
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'omt = omt.main:main',
        ],
    }
)
