from setuptools import setup, find_packages

setup(
    name="ai_security_tool",
    version="2.0",
    packages=find_packages(),
    install_requires=[
        'ast',
        'datetime',
        're',
        'json',
        'threading',
        'time'
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered security tool for automatic error detection and fixing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai_security_tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
