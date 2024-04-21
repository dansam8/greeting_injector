from setuptools import setup, find_packages

setup(
    name='greeting_injector',
    version='0.0.1',
    author='Daniel Samuelson',
    description='A package for overlaying a pre-recorded greeting into microphone input.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'sounddevice',
        'wavio'

    ],
    entry_points={
        'console_scripts': [
            'greeting_injector = greeting_injector.main:main'
        ]
    },
    python_requires='>=3.8',
)
