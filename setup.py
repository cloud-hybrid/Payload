import setuptools

with open("README.md", "r") as file:
  long_description = file.read()

setuptools.setup(
  name="Vault",
  version="0.0.1",
  author="Jacob B. Sanders",
  author_email="development.cloudhybrid@gmail.com",
  description="IaaS Automation and Management Tools",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/cloud-hybrid/Cloud",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Linux",
  ],
)