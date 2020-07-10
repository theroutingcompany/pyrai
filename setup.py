# from setuptools import setup

# setup(name="pyrai",
#       packages=["pyrai"],
#       include_package_data=True,
#     #   install_requires=[
#           # Dependencies go here...
#     #   ]
#  )
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrai", # Replace with your own username
    version="0.0.3",
    author="Routable AI",
    author_email="eng@routable.ai",
    description="A Python library for the Routable AI API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/routable-ai/pyrai",
    packages=setuptools.find_packages(),
    install_requires=[
          "ipython",
          "plotly",
          "python-dateutil",
          "pytimeparse",
          "requests"
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
