# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys
import inspect
import logging

import salt.netapi
import salt.scripts
from salt.ext import six
import salt.utils.parsers
from salt.scripts import _install_signal_handlers

log = logging.getLogger(__name__)


def sapi_sproxy(
    self, tgt, fun, tgt_type='glob', timeout=None, full_return=False, **kwargs
):
    '''
    Shortcut to invoke an arbitrary Salt function via sproxy.
    '''
    kwargs.update(
        {
            'function': fun,
            'tgt': tgt,
            'tgt_type': tgt_type,
            'static': True,
            'sync_roster': True,
        }
    )
    return salt.netapi.NetapiClient.runner(
        self, 'proxy.execute', timeout=timeout, full_return=full_return, **kwargs
    )


def sapi_sproxy_async(
    self, tgt, fun, tgt_type='glob', timeout=None, full_return=False, **kwargs
):
    '''
    Shortcut to invoke an arbitrary Salt function via sproxy, asynchronously.
    '''
    kwargs.update(
        {
            'function': fun,
            'tgt': tgt,
            'tgt_type': tgt_type,
            'static': True,
            'sync_roster': True,
        }
    )
    return salt.netapi.NetapiClient.runner_async(
        self, 'proxy.execute', timeout=timeout, full_return=full_return, **kwargs
    )


salt.netapi.NetapiClient.sproxy = sapi_sproxy
salt.netapi.NetapiClient.sproxy_async = sapi_sproxy_async
salt.netapi.CLIENTS = [
    name
    for name, _ in inspect.getmembers(
        salt.netapi.NetapiClient, predicate=inspect.ismethod if six.PY2 else None
    )
    if not (name == 'run' or name.startswith('_'))
]
salt.utils.parsers.SaltAPIParser.description = (
    'salt-sapi is an enhanced Salt API system that provides additional '
    'sproxy and sproxy_async clients, to simplify the usage of salt-sproxy '
    'through the Salt REST API'
)
salt.utils.parsers.SaltAPIParser.epilog = (
    'You can find additional help about %prog issuing "man %prog" '
    'or on https://salt-sproxy.readthedocs.io/ and '
    'https://docs.saltstack.com/en/latest/ref/cli/salt-api.html.'
)


def salt_sapi():
    '''
    The main function for salt-sapi.
    '''
    salt.scripts.salt_api()


def salt_sproxy():
    '''
    Execute a salt convenience routine.
    '''
    import salt_sproxy.cli

    if '' in sys.path:
        sys.path.remove('')
    client = salt_sproxy.cli.SaltStandaloneProxy()
    _install_signal_handlers(client)
    client.run()


if __name__ == '__main__':
    salt_sproxy()
