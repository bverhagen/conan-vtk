#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from conans import ConanFile, CMake, tools
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def configure_cmake(self):
        cmake = CMake(self, 'Ninja')
        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.definitions['BUILD_DOCUMENTATION'] = False
        cmake.definitions['BUILD_EXAMPLES'] = True
        cmake.definitions['BUILD_MATLAB_BINDINGS'] = False
        cmake.definitions['VTK_WRAP_PYTHON'] = False
        cmake.definitions['BUILD_TESTING'] = False
        cmake.definitions['VTK_Group_Qt'] = self.options.with_qt
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = CMake(self, 'Ninja')
        cmake.configure()
        cmake.build()

    def test(self):
        bin_path = os.path.join("bin", "test_package")
        self.run(bin_path, run_environment=True)
