from setuptools import setup, find_packages

setup(
    name="sirjna",
    version="0.1.1",
    description="Sirjna — Frappe v15 MVP app (esbuild-safe)",
    author="Parinda LLC",
    author_email="contact@sirjna.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)