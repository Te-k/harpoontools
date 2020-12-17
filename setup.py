from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='harpoontools',
    version='0.1.6',
    description='CLI tools going with Harpoon',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Te-k/harpoontools',
    author='Tek',
    author_email='tek@randhome.io',
    keywords='osint',
    include_package_data=True,
    install_requires=[
        'requests',
        'harpoon==0.1.6'
    ],
    python_requires='>=3.5',
    license='GPLv3',
    packages=['harpoontools'],
    entry_points= {
        'console_scripts': [
            'ipinfo=harpoontools.tools:ipinfo',
            'asninfo=harpoontools.tools:asninfo',
            'dns=harpoontools.tools:dns',
            'asncount=harpoontools.tools:asncount',
            'countrycount=harpoontools.tools:countrycount',
            'htraceroute=harpoontools.tools:traceroute',
            'myip=harpoontools.tools:myip'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]

)
