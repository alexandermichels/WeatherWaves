import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WeatherWaves",
    version="0.0.1",
    author="Alexander Michels",
    author_email="alexandercm4297@gmail.com",
    description="A package for responding to the weather",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexandermichels/WeatherWaves",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)