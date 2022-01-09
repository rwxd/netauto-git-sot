from pathlib import Path
import logging
from typing import List, Callable
from eve.classifier import Classifier
from eve.jerakia import Jerakia
from eve.jinja.renderer import TemplateRenderer
import sys
import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from eve.logging import logger
from eve.models.build import Template
import os


def build(request, plugin, template_render, device):
    '''Build the provided device'''
    templates = plugin.jerakia.lookup(device, namespace="build", key="templates")
    if not templates:
        pytest.skip(f'No templates defined or found for {device}')
    for template in templates:
        logger.info(
            f'Building template {template.source} to {template.destination} for {device}'
        )
        template_render(device, template)
    if not plugin.skip_checks:
        checks = plugin.jerakia.lookup(device, namespace="build", key="checks")
        for check in checks:
            logger.info(f'Running check {check.script} for {device}')
            os.system(f'{check.script} {device}')


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
        jerakia: Jerakia,
        classifier: Classifier,
    ):
        self.renderer = TemplateRenderer(
            basepath=templates,
            devices=[d.name for d in devices],
            cache=cache,
            classifier=classifier,
            jerakia=jerakia,
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
    def template_render(self) -> Callable[[str, Template], None]:
        def _render(device: str, template: Template) -> None:
            result = self.renderer.render(template.source, device)
            if not result or not result.strip():
                logger.info(f'skip empty template {device} for {template.source}')
                return
            output_file = self.output.joinpath(device).joinpath(template.destination)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w") as f:
                f.write(result)

        return _render

    @pytest.fixture(scope="session")
    def plugin(self):
        return self
