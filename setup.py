from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dev_2",
    use_scm_version=True,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],  
    description="Bibliothèque Python pour des jeux de plateau",
    long_description=long_description,  
    long_description_content_type="text/markdown",  
    author="Alex",
    author_email="Alexisjacobs@protonmail.com",
    url="https://github.com/Ajkll/dev2_jeux_plateau_prod",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "dev2=app.main:main", 
        ]
    },
)
