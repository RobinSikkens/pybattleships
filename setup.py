from setuptools import setup

from bottleships import VERSION

setup(name='bottleships',
      version=VERSION,
      description='A Python Battleship framework',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
      ],
      keywords='sticky woestgaaf battleship',
      url='http://github.com/RobinSikkens/bottleships',
      author='Robin Sikkens & Maarten van den Berg',
      author_email='bottleships@robinsikkens.nl',
      license='MIT',
      packages=['bottleships'],
      install_requires=[
      ],
      include_package_data=True,
      zip_safe=False
)
