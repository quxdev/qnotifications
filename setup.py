from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name='qnotifications',
    version='0.1.0',
    description='A simple wrapper for AWS SNS',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='quxdev',
    author_email='quxdev@gmail.com',
    url='https://github.com/quxdev/qnotifications',  # Updated URL
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.12",
)
