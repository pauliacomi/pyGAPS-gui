from setuptools import setup
from setuptools import find_packages

if __name__ == "__main__":

    setup(
        packages=find_packages(),
        package_data={'pygapsgui': ['resources/*']},
        entry_points={'console_scripts': ['pygapsgui=pygapsgui:main']},
    )
