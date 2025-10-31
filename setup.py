from setuptools import setup, find_packages

with open("README.md", "w", encoding="utf-8") as f:
    f.write("# Sirjna\n\nGenerated bundle for Frappe v15 demo.")

setup(
    name="sirjna",
    version="0.10.0",
    description="Sirjna – mentorship portal for Frappe v15",
    author="Sirjna Mentorship",
    author_email="support@sirjna.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)