"""setup"""

from setuptools import setup, find_packages

requirements = [
    'numpy',
    'json',
    'csv',
    'scipy',
]



setup(
    author='DESC/SLSC',
    author_email='h.best99999@gmail.com',
    python_requirements='>=3.7',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    description='LSST live light curve monitoring pipeline',
    install_requirements=requirements,
    license='MIT license',
    include_package_data=True,
    keywords='livelcs',
    name='livelcs',
    packages=find_packages(
        where=['src'],
        include=[
            'livelcs',
            'livelcs*',
        ]
    ),
    test_suite='tests',
    url='',
    version='0.1.0',
)

    
