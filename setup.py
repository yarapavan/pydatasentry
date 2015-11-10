from setuptools import setup

setup(name='pydatasentry',
      version='0.1-alpha',
      description='Memory tool for Python-Based Data Science',
      url='http://github.com/FourthLion/pydatasentry',
      download_url='https://github.com/FourthLion/pydatasentry/tarball/0.1-alpha',
      author='Venkata Pingali',
      author_email='pingali@gmail.com',
      packages=['pydatasentry'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Scientific/Engineering :: Information Analysis'
      ],
      keywords=['pydata', 'pandas', 'documentation', 
                'regressions', 'tool'],
      install_requires=[
          "glob2>=0.4.1",
          "numpy>=1.9.1",
          "pandas>=0.15.1",
          "patsy>=0.4.0",
          "scikit-learn>=0.16.1",
          "scipy>=0.16.0",
          "six>=1.8.0",
          "sklearn>=0.0",
          "statsmodels>=0.6.1"
      ],
      license='MIT',
      )
