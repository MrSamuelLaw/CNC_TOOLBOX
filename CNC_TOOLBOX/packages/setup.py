import setuptools

setuptools.setup(
    name="cnc_toolbox_packages",
    version="0.0.1",
    author="samuel law",
    description="package for parsing various flavors of gcode",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)
