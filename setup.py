from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()

setup(
    name="sirjna",
    version="0.1.0",
    description="Sirjna – Frappe v15 mentorship app (MVP)",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="Parinda LLC",
    author_email="contact@sirjna.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)
