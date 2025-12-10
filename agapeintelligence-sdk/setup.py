from setuptools import setup, find_packages

setup(
    name="agapeintelligence",
    version="0.1.0",
    packages=find_packages(),
    description="Unified AgapeIntelligence SDK",
    install_requires=[
        "numpy",
        "scipy",
        "astropy",
    ],
)
