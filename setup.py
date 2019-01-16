import setuptools

setuptools.setup(
    name='DataDeDup',
    version='0.0.1',
    py_modules=setuptools.find_packages(),
    install_requires=[
        'Click',
        'jsonpickle'
    ],
    entry_points='''
        [console_scripts]
        DataDeDup=DataDeDup:cli
    ''',
)