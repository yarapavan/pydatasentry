from setuptools import setup

setup(name='pydatasentry',
      version='0.1.4',
      description='Memory tool for Python-Based Data Science',
      url='http://github.com/FourthLion/pydatasentry',
      download_url='https://github.com/FourthLion/pydatasentry/tarball/0.1.4',
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
      scripts=['bin/sentry.py'],
      #data_files=[
      #    ('share', ['share/basic_ols.py.template', 
      #               'share/sentry-conf.py.template'])
      #],
      package_data={
          'pydatasentry': ['share/*template']
      },
      install_requires=[
      ],
      license='MIT',
      )
