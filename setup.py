import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hdxpyutils",
    version="1.0.2",
    author="Hashdex",
    author_email="tech@hashdex.com",
    description="A package containing utilities functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests==2.31.0",
        "boto3==1.16.18",
        "numpy==1.22.0",
        "pandas==1.1.4",
        "pyathena==2.0.0",
        "s3fs==0.3.5",
        "openpyxl==3.0.7",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
