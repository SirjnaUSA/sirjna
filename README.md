with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sirjna",
    version="0.1.0",
    description="Sirjna – mentorship portal for engineering MS (US/Canada)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
