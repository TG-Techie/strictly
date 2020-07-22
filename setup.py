import setuptools
import strictly

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="strictly",
    version=strictly.__version__,
    author="Jonah Yolles-Murphy",
    author_email="jonahym@mitre.org",
    description="A run-time tool to enforce strict typing in python using type hints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TG-Techie/strictly",
    py_modules=['strictly'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
