from setuptools import setup, find_packages


setup(
    name='Job Cloud',
    author='Matt Goodnight',
    author_email='mbgoodnight@gmail.com',
    packages=find_packages(exclude=["dev-bin", "docs"]),
    install_requires=['numpy', 'Pillow', 'wordcloud'],
    tests_requires=['pytest'],
    include_package_data=True,
    version='0.2',
    license='MIT',
    description='Word cloud generator for job listings'
)
