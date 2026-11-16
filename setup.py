from setuptools import setup, find_packages

setup(
    name="python_crypto_orderbook_matching_engine",
    version="1.0.0",
    description="Python Crypto Orderbook Matching Engine - Production Grade Python Engine",
    author="Shyamkumar Pandey",
    author_email="shyampandey1104@gmail.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=["pytest>=7.0.0"]
)
