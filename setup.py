from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        version='1.0.0',
        url='https://github.com/GustavoJST/PelandoBot',
        packages=find_packages(where="src"),
        package_dir={"": "src"},
    )