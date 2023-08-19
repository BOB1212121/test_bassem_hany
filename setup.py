from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in test_bassem_hany/__init__.py
from test_bassem_hany import __version__ as version

setup(
	name="test_bassem_hany",
	version=version,
	description="Task Solution",
	author="Bassem Hany",
	author_email="bassem5656567@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
