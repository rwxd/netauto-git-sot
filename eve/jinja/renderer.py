from jinja2 import TemplateRuntimeError
from jinja2.loaders import FileSystemLoader
from jinja2.nodes import CallBlock
from jinja2.ext import Extension
from jinja2 import Environment, contextfilter, contextfunction
from jinja2.nativetypes import NativeEnvironment
from typing import Union, List
from collections import OrderedDict
from eve.jinja.filters import imported_jinja_filters, registered_jinja_filters
from pathlib import Path

# Stolen from https://stackoverflow.com/questions/21778252/how-to-raise-an-exception-in-a-jinja2-macro
class ErrorExtension(Extension):
    '''Extension providing {% error %} tag, allowing to raise errors
    directly from a Jinja template.
    '''

    tags = frozenset(['error'])

    def parse(self, parser):
        """Parse the {% error %} tag, returning an AST node."""
        lineno = next(parser.stream).lineno
        message = parser.parse_expression()
        node = CallBlock(
            self.call_method('_raise', [message], lineno=lineno),
            [],
            [],
            [],
            lineno=lineno,
        )
        return node

    def _raise(self, message, caller):
        """Execute the {% error %} statement, raising an exception."""
        raise TemplateRuntimeError(message)


class TemplateRenderer(object):
    '''Build Jinja templates.'''

    def __init__(self, basepath: Path, devices: List[Path], cache: bool):
        self.env = self._build_env(basepath, Environment)
        self.native_env = self._build_env(basepath, NativeEnvironment)
        self.devices = devices
        self.cache = cache

    def _build_env(
        self, basepath: Path, constructor: Union[Environment, NativeEnvironment]
    ) -> Union[Environment, NativeEnvironment]:
        '''Creates environment variables for Jinja2 template rendering'''
        env = constructor(
            loader=FileSystemLoader(str(basepath)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            extensions=[ErrorExtension, 'jinja2.ext.do'],
        )

        # import jinja filters
        for module, fs in imported_jinja_filters:
            for f in fs:
                try:
                    fn, name = f
                except ValueError:
                    fn, name = f, f
                env.filters[name] = getattr(module, fn)

        # register filters
        for function in registered_jinja_filters:
            env.filters[function.__name__] = f
        env.filters['store'] = self._store_set

        # register custom global functions
        env.globals['store'] = self._store_get

    @contextfilter
    def _store_set(self, ctx, value, key: str, *args):
        '''Save arbitrary data to an internal store. The value stored is
        prefixed by the current device name and suffixed by additional
        arguments.'''
        self.store[key].append((ctx.parent["device"], value, *args))
        return value

    def _store_get(self, key: str) -> List:
        '''Retrieves data from the interal store.'''
        return list(OrderedDict.fromkeys(self.store[key]))
