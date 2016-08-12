from setuptools import setup

setup(
	name="Pman",
	verion="1.0",
	py_modules=["pman"],
	install_requires=[
		"Click"
	],
	entry_points={
		'console_scripts': [
			'pman = pman:cli',
		]
	}
)
