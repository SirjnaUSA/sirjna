from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sirjna",
    version="0.1.0",
    description="Sirjna — Honest, data-based mentorship (Frappe v15 app)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Parinda LLC",
    author_email="contact@sirjna.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "requests>=2.31.0",
    ],
)
