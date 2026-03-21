"""Setup configuration for FlaschenTaschen Python port."""

from setuptools import find_packages, setup

setup(
    name="flaschen-taschen-py",
    version="0.1.0",
    description="Python port of FlaschenTaschen display control library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ported to Python",
    url="https://github.com/FlaschenTaschen/ft-py",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "send-text=flaschen_taschen.cli.send_text:main",
            "send-image=flaschen_taschen.cli.send_image:main",
            "send-video=flaschen_taschen.cli.send_video:main",
            "ft-debugger=flaschen_taschen.cli.ft_debugger:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "black>=21.0",
            "isort>=5.9",
            "flake8>=3.9",
        ],
        "image": ["Pillow>=8.0"],
        "video": ["ffmpeg-python>=0.2.1"],
        "numpy": ["numpy>=1.20"],
        "midi": ["mido>=1.2.9"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
    ],
)
