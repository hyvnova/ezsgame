
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(
        r"__pycache__",
        language_level = "3",
        quiet = True
    )
)
