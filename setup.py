import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Hash-byte-Dedupe",
    version="0.0.1",
    author="Nathan Tamez",
    author_email="jamestamezn@gmail.com",
    description="A simple project that uses matching hash to find exact maches of files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NatoNathan/Hash-byte-Dedupe",
    py_modules=setuptools.find_packages(),
    packages=setuptools.find_packages(),
    install_requires=[
        'Click',
        'jsonpickle'
    ],
    entry_points='''
        [console_scripts]
        HashByteDedupe=HashByteDedupe:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)