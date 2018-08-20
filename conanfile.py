#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import glob


class LibnameConan(ConanFile):
    name = "vtk"
    version = "6.3.0"
    description = "Visualization Toolkit"
    url = "https://github.com/bverhagen/conan-vtk"
    homepage = "https://gitlab.kitware.com/vtk/vtk"
    author = "Bart Verhagen <barrie.verhagen@gmail.com>"
    # Indicates License type of the packaged library
    license = "BSD-3-Clause"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "with_qt": [True, False]}
    default_options = "shared=False", "fPIC=True", "with_qt=False"

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    # Use version ranges for dependencies unless there's a reason not to
    # Update 2/9/18 - Per conan team, ranges are slow to resolve.
    # So, with libs like zlib, updates are very rare, so we now use static version


    requires = (
    )

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://gitlab.kitware.com/vtk/vtk"
        tools.get("{0}/-/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-v" + self.version

        #Rename to "source_subfolder" is a convention to simplify later steps
        for source_name in glob.glob(extracted_dir + "*"):
            os.rename(source_name, self.source_subfolder)

    def configure_cmake(self):
        cmake = CMake(self, 'Ninja')
        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.definitions['BUILD_DOCUMENTATION'] = False
        cmake.definitions['BUILD_EXAMPLES'] = False
        cmake.definitions['BUILD_MATLAB_BINDINGS'] = False
        cmake.definitions['VTK_WRAP_PYTHON'] = False
        cmake.definitions['BUILD_TESTING'] = False
        cmake.definitions['VTK_Group_Qt'] = self.options.with_qt
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can just remove the lines below
        include_folder = os.path.join(self.source_subfolder, "include")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = ['include/vtk-6.3']
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.libdirs = ['lib']
        self.cpp_info.bindirs = ['bin']
