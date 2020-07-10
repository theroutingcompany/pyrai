# from setuptools import setup

# setup(name="pyrai",
#       packages=["pyrai"],
#       include_package_data=True,
#     #   install_requires=[
#           # Dependencies go here...
#     #   ]
#  )
import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrai", # Replace with your own username
    version="0.0.0",
    author="Routable AI",
    author_email="nathan@routable.ai",
    description="A Python library for the Routable AI API",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/routable-ai/pyrai",
    packages=setuptools.find_packages(),
    install_requires=[
          "ipython", 
          "plotly", 
          "python-dateutil",
          "pytimeparse"
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)