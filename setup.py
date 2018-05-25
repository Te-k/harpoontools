from setuptools import setup

setup(
    name='harpoontools',
    version='0.1.1',
    description='CLI tools going with Harpoon',
    url='https://github.com/Te-k/harpoontools',
    author='Tek',
    author_email='tek@randhome.io',
    keywords='osint',
    include_package_data=True,
    dependency_links=[
        'git+https://github.com/Te-k/harpoon.git@master',
    ],
    install_requires=[
        'harpoon'
    ],
    python_requires='>=3.5',
    license='GPLv3',
    packages=['harpoontools'],
    #package_dir={'harpoon.lib': 'harpoon/lib'},
    #package_data={'harpoon': ['harpoon/data/*.conf']},
    entry_points= {
        'console_scripts': [
            'ipinfo=harpoontools.tools:ipinfo',
            'asninfo=harpoontools.tools:asninfo',
            'dns=harpoontools.tools:dns',
            'asncount=harpoontools.tools:asncount',
            'countrycount=harpoontools.tools:countrycount',
        ]
    }
)
