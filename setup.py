from setuptools import setup

setup(
    name="drawtext",
    version="0.0.1",
    install_requires=["pathlib", "Pillow"],
    packages = ['src', ],
    package_data = {'src':['NotoSerifCJKjp-Black.otf',]},
    entry_points={
        "console_scripts": [
            "drawtext = src.drawtext:main",
        ],
    }
)

