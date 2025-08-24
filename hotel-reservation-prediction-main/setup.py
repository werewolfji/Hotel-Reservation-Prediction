from setuptools import setup,find_packages

with open ("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="hotel-reservation-1",
    version="0.1",
    author="GopalaKrishnaAbba",
    packages=find_packages(),
    install_requires = requirements,
)
