from setuptools import setup, find_packages

setup(
    name="agape-unified",
    version="1.0.0",
    description="Unified AgapeIntelligence Framework",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "jax[cpu]",
        "qutip",
        "numpy",
        "scipy",
        "gradio",
        "httpx",
    ],
)
