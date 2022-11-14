from setuptools import find_packages, setup

setup(
	name="szurubooru.py",
	packages=find_packages(include=["szurubooru"]),
	version="0.1.0",
	description="A Python API wrapper for Szurubooru",
	author="SauceyRed",
	author_email="csred@protonmail.com",
	license="GPLv3",
	classifiers=[
		"Environment :: Console",
		"Intended Audience :: Developers",
		"License :: OSI Approved",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		"Natural Language :: English",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.11"
	]
)
