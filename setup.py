from setuptools import setup, find_packages

setup(
    name='draedon',
    version='1.0',
    py_modules=['main'], 
    packages=find_packages(),
    install_requires=[
        'rich',
        'inquirer', #strelochki
    ],
    entry_points={
        'console_scripts': [
            'draedon = main:main', 
        ],
    },
)