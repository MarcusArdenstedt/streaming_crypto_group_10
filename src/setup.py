from setuptools import setup
from setuptools import find_packages



print(find_packages())

setup(
    name="coin_project",
    version="0.0.1",
    description="""test package install""",
    author="Marcus, Andreas, Mustafa, Jie",
    author_email="YOUR_EMAIL@mail.com",
    install_requires=[],
    packages=find_packages(exclude=("EDA")),
    # entry_points={"console_scripts": ["dashboard = utils.run_dashboard:run_dashboard"]},
)