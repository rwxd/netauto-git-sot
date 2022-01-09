from pathlib import Path
import logging
from typing import List
from eve.jerakia import Jerakia
from eve.jinja.renderer import TemplateRenderer
import sys
import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from eve.logging import logger
import os


def build(request, plugin, template_render, device):
    '''Build the provided device'''
    templates = plugin.jerakia.lookup(device, namespace="build", key="templates")


class PytestPlugin:
    def __init__(
        self,
        *,
        templates,
        output: Path,
        skip_checks: bool,
        diff: bool,
        cache: bool,
        devices: List[Path],
        targets: List[Path],
        debug: bool,
        silent: bool,
        jerakia: Jerakia
    ):
        self.renderer = TemplateRenderer(
            basepath=templates,
            devices=devices,
            cache=cache,
        )
        self.jerakia = jerakia
        self.output = output
        self.targets = targets
        self.cache = cache
        self.skip_checks = skip_checks
        self.diff = diff
        self.debug = debug
        self.silent = silent

    def pytest_load_initial_conftests(
        self, early_config: Config, parser: Parser, args: List[str]
    ):
        # remove logging
        root = logging.getLogger("")
        root.handlers = [h for h in root.handlers if not hasattr(h, "eve")]

        # core configuration
        early_config.addinivalue_line("python_functions", "build")
        args += [
            "-v",
            "--showlocals",
            "--log-level=debug" if self.debug else "--log-level=info",
            "--tb=short" if self.silent else "--tb=long" if self.debug else "--tb=auto",
        ]
        # Configure plugins
        args += [
            "--html",
            str(self.output.joinpath("report.html")),
            "--self-contained-html",
        ]
        args += ["--junitxml", str(self.output.joinpath("junit.xml"))]
        # Add ourselve as the file to test
        args += [sys.modules[__name__].__file__]

    def pytest_generate_tests(self, metafunc):
        if 'device' in metafunc.fixturenames:
            return metafunc.parametrize('device', [p.name for p in self.targets])

    @pytest.fixture(scope='session')
    def template_render(self):
        def _render(device, template):
            result = self.renderer.render(template["name"], device)
            if not result or not result.strip():
                logger.info(
                    "skip empty template {} for {}".format(device, template["name"])
                )
                return
            output_file = self.output.joinpath(device.name).joinpath(
                template['destination']
            )
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w") as f:
                f.write(result)

        return _render

    @pytest.fixture(scope="session")
    def plugin(self):
        return self
