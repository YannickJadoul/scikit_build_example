# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

try:
    from skbuild import setup
except ImportError:
    print(
        "Please update pip, you need pip 10 or greater,\n"
        " or you need to install the PEP 518 requirements in pyproject.toml yourself",
        file=sys.stderr,
    )
    raise


def patched_WindowsPlatform_init(self):
	import textwrap
	from skbuild.platform_specifics.windows import WindowsPlatform, CMakeVisualStudioCommandLineGenerator, CMakeVisualStudioIDEGenerator

	super(WindowsPlatform, self).__init__()

	self._vs_help = textwrap.dedent("""
		Building Windows wheels for requires Microsoft Visual Studio 2017 or 2019:

		  https://visualstudio.microsoft.com/vs/
		""").strip()

	supported_vs_years = [("2019", "v141"), ("2017", "v141")]
	for vs_year, vs_toolset in supported_vs_years:
		self.default_generators.extend([
			CMakeVisualStudioCommandLineGenerator("Ninja", vs_year, vs_toolset),
			CMakeVisualStudioIDEGenerator(vs_year, vs_toolset),
			CMakeVisualStudioCommandLineGenerator("NMake Makefiles", vs_year, vs_toolset),
			CMakeVisualStudioCommandLineGenerator("NMake Makefiles JOM", vs_year, vs_toolset)
		])

import skbuild.platform_specifics.windows
skbuild.platform_specifics.windows.WindowsPlatform.__init__ = patched_WindowsPlatform_init


setup(
    name="scikit_build_example",
    version="0.0.1",
    description="a minimal example package (with pybind11)",
    author="Henry Schreiner",
    license="MIT",
    packages=["scikit_build_example"],
    package_dir={"": "src"},
    cmake_install_dir="src/scikit_build_example",
)
