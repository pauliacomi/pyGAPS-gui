from setuptools import setup
from setuptools import find_packages

requirements = [
    # TODO: put your package requirements here
    'PySide2',
]

setup(
    name='pygaps-gui',
    version='0.0.1',
    license='GPLv3',
    author="Paul Iacomi",
    author_email='iacomi.paul@gmail.com',
    description="Simple GUI for pyGAPS",
    url='https://github.com/pauliacomi/pyGAPS-gui',
    packages=find_packages(),
    # ['pygaps-gui', 'pygaps-gui.gui'],
    package_data={'pygaps-gui': ['resources/*']},
    entry_points={
        'console_scripts': [
            'pygaps-gui=pygaps-gui.app:main'
        ]
    },
    install_requires=requirements,
    zip_safe=False,
    keywords='application',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
