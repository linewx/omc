from setuptools import setup, find_packages
install_requires = [
    'requests>=2.22.0',
    'dynaconf[all]>=2.2.3',
    'pyfiglet>=0.8.post1',
    'Click>=7.0',
    'psutil>=5.5',
    'ruamel.yaml>=0.16.12',
    'prettytable>=0.7.2'
]


setup(
    name='omc',
    version="0.2.1",
    description='oh my command',
    license='MIT',
    author='Lu Ganlin',
    author_email='linewx1981@gmail.com',
    url='https://github.com/linewx/omc',
    packages=find_packages(),
    package_data={'omc.config': ['*.yaml'], 'omc.lib': ['**', '**/*', '**/**/*']},
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'omc = omc.main:main',
        ],
    }
)
