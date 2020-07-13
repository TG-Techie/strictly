import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-YOUR-USERNAME-HERE", # Replace with your own username
    version="0.0.1",
    author="Jonah Yolles-Murphy",
    author_email="jonahym@mitre.org",
    description="A run-time tool to enforce strict typing in python using type hints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="github.com/TG-Techie/strictly",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
