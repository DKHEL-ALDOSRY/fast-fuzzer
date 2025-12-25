from setuptools import setup

setup(
    name='fast-fuzzer',
    version='1.0.0',
    description='High-performance async fuzzer',
    long_description='Fast-Fuzzer tool for directory discovery',
    long_description_content_type='text/plain',
    author='DKHEL ALDOSRY',
    py_modules=['fuzzer'],
    install_requires=['aiohttp', 'colorama', 'urllib3'],
    entry_points={
        'console_scripts': [
            'fast-fuzzer = fuzzer:main_entry',
        ],
    },
    python_requires='>=3.7',
)