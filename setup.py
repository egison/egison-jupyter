from setuptools import setup, find_packages


setup(name='egison_kernel',
      version='0.1.0',
      description='Egison 5 Kernel for Jupyter Notebook',
      install_requires=[
          'ipykernel',
          'pexpect',
          'future'
      ],
      author='Satoshi Egi',
      author_email='egi@egison.org',
      url='https://github.com/egison/egison_kernel',
      packages=find_packages(),
      entry_points="""
      [console_scripts]
      """,)
