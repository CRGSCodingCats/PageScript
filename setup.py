from setuptools import setup, find_packages

setup(
    name="pagescript",
    version="0.1.2-alpha",
    description="A beginner-friendly markup language that converts simple syntax into full HTML pages.",
    author="Coding Cats",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pagescript=pagescript.converter:main'
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)
