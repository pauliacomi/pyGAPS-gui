from setuptools import setup
from setuptools import find_packages

setup(
    name='pygapsgui',
    use_scm_version={
        'local_scheme': 'dirty-tag',
        'write_to': 'pygapsgui/_version.py',
        'fallback_version': '0.1.0',
    },
    license='MIT license',
    description="GUI for pyGAPS",
    author="Paul Iacomi",
    author_email='mail@pauliacomi.com',
    url='https://github.com/pauliacomi/pyGAPS-gui',
    packages=find_packages(),
    package_data={'pygapsgui': ['resources/*']},
    entry_points={'console_scripts': ['pygapsgui=pygapsgui:main']},
    classifiers=[  # Classifier list at https://pypi.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Chemistry',
    ],
    keywords=['adsorption', 'characterization', 'porous materials'],
    python_requires='>=3.8',
    install_requires=[
        'pyside6',
        'qtpy',
        'pygaps',
    ],
    setup_requires=[
        'setuptools_scm',
        'pyinstaller > 4.0'
    ]
)
