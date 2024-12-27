from setuptools import setup, find_packages

setup(
    name="dev_2",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],  # Utiliser requirements.txt si nécessaire
    description="dev2_jeux_de_plateau",
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
            "dev2=app.main:main",  # Permet d'exécuter `dev2` dans le terminal
        ]
    },
)
