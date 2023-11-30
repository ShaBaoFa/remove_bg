from setuptools import setup, find_packages

setup(
    name='remove_bg_with_oss',  # Replace with your project's name
    version='0.1.0',  # Project version
    author='ShaBaoFa',  # Replace with your name
    author_email='wlfpanda1012@gmail.com',  # Replace with your email
    description='remove bg',  # Project description
    long_description=open('README.md').read(),  # Long description read from the the readme file
    long_description_content_type='text/markdown',
    url='https://github.com/ShaBaoFa/remove_bg',  # Replace with your project's url
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'Pillow',  # Example dependency, replace with your project's dependencies
        'requests',
        'oss2',
        'alibabacloud-sts20150401',
        'python-dotenv',
        # Add other dependencies as needed
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum version requirement of the package
    # Additional arguments can be added as needed
)
