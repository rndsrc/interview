# Copyright (C) 2017 Chi-kwan Chan
# Copyright (C) 2017 Harvard-Smithsonian Center for Astrophysics
#
# This file is part of interview.
#
# Interview is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Interview is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with interview.  If not, see <http://www.gnu.org/licenses/>.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name    = "interview",
    version = "0.0b0",

    description      = "Interview: an interactive data viewing and inspecting framework",
    long_description = "Interview is an interactive data viewing and inspecting framework for the Event Horizon Telescope.",

    author       = "Phani Datta Velicheti,Chi-kwan Chan",
    author_email = "[phaniv@email.arizona.edu","ckchan@cfa.harvard.edu"],
    license      = "GPLv3+",
    url          = "https://github.com/phanicode/interview,https://github.com/rndsrc/interview",
    classifiers  = [,
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],

    packages         = ["interview"],
    install_requires = ["pandas", "bokeh"],
)
