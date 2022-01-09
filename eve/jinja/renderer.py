from jinja2 import TemplateRuntimeError
from jinja2.loaders import FileSystemLoader
from jinja2.nodes import CallBlock
from jinja2.ext import Extension
from jinja2 import Environment, contextfilter, contextfunction
from jinja2.runtime import Context
from jinja2.nativetypes import NativeEnvironment
from typing import Union, List
from collections import OrderedDict
from eve.classifier import Classifier
from eve.jerakia import Jerakia
from eve.jinja.filters import imported_jinja_filters, registered_jinja_filters
from pathlib import Path
from eve.structure import find_host_dir

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

    def __init__(
        self,
        basepath: Path,
        devices: List[str],
        cache: bool,
        classifier: Classifier,
        jerakia: Jerakia,
    ):
        self._devices = devices
        self.cache = cache
        self.classifier = classifier
        self.jerakia = jerakia
        self.env = self._build_env(basepath, Environment, classifier)
        self.native_env = self._build_env(basepath, NativeEnvironment, classifier)

    def _build_env(
        self,
        basepath: Path,
        constructor: Union[Environment, NativeEnvironment],
        classifier: Classifier,
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
        env.globals["scope"] = classifier.scope
        env.globals["lookup"] = self._lookup
        env.globals["devices"] = self._devices
        env.globals["store"] = self._store_get
        return env

    def render(self, name: str, device: str) -> None:
        '''Render a template.
        The `scope` will be reachable trough the contexts `parent` attribute.
        '''
        template = self.env.get_template(name)
        scope = self.classifier.scope(find_host_dir(device))
        return template.render(device=device, **scope)

    @contextfunction
    def _lookup(self, ctx: Context, namespace: str, key: str, device=None):
        '''Allows to lookup jerakia data from within a Jinja template.'''
        if device is None:
            device = ctx.parent['device']
        value = self.jerakia.lookup(device, namespace, key)
        return value

    @contextfilter
    def _store_set(self, ctx: Context, value, key: str, *args):
        '''Save arbitrary data to an internal store. The value stored is
        prefixed by the current device name and suffixed by additional
        arguments.'''
        self.store[key].append((ctx.parent["device"], value, *args))
        return value

    def _store_get(self, key: str) -> List:
        '''Retrieves data from the interal store.'''
        return list(OrderedDict.fromkeys(self.store[key]))
