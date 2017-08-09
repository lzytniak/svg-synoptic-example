#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="taurusgui-synoptic",
    version="1.1.0",
    description="Example SVG synoptic for a beamline",
    author="Lukasz Zytniak",
    author_email="lzytniak",
    license="GPLv3",
    packages=find_packages(),
    package_data={'synoptic': ['*.css', '*.svg', '*.html', 'images/*.png']},
    data_files=[("share/applications", ["synoptic.desktop"])],
    scripts=["scripts/ctsynoptic"]
)
