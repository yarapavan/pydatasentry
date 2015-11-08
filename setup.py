from setuptools import setup

setup(name='pydatasentry',
      version='0.1',
      description='Capture modeling input and output',
      url='http://github.com/pingali/pydatasentry',
      author='Venkata Pingali',
      author_email='pingali@gmail.com',
      packages=['pydatasentry'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3 :: Only'
          'Topic :: Scientific/Engineering :: Information Analysis'
      ],
      keywords='funniest joke comedy flying circus',
      license='MIT',
      install_requires=[
      ],
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      )
