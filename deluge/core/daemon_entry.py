# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2010 Pedro Algarvio <pedro@algarvio.me>
#
# This file is part of Deluge and is licensed under GNU General Public License 3.0, or later, with
# the additional special exception to link portions of this program with the OpenSSL library.
# See LICENSE for more details.
#


import os
import sys
from logging import FileHandler, getLogger

from deluge.common import run_profiled
from deluge.configmanager import get_config_dir
from deluge.ui.baseargparser import BaseArgParser
from deluge.ui.util import lang


def add_daemon_options(parser):
    group = parser.add_argument_group(_('Daemon Options'))
    group.add_argument('-u', '--ui-interface', metavar='<ip-addr>', action='store',
                       help=_('IP address to listen for UI connections'))
    group.add_argument('-p', '--port', metavar='<port>', action='store', type=int,
                       help=_('Port to listen for UI connections on'))
    group.add_argument('-i', '--interface', metavar='<ip-addr>', dest='listen_interface', action='store',
                       help=_('IP address to listen for BitTorrent connections'))
    group.add_argument('--read-only-config-keys', metavar='<comma-separated-keys>', action='store',
                       help=_('Config keys to be unmodified by `set_config` RPC'), type=str, default='')
    parser.add_process_arg_group()


def start_daemon(skip_start=False):
    """
    Entry point for daemon script

    Args:
        skip_start (bool): If starting daemon should be skipped.

    Returns:
        deluge.core.daemon.Daemon: A new daemon object

    """
    lang.set_dummy_trans(warn_msg=True)

    # Setup the argument parser
    parser = BaseArgParser()
    add_daemon_options(parser)

    options = parser.parse_args()

    # Check for any daemons running with this same config
    from deluge.core.daemon import is_daemon_running
    pid_file = get_config_dir('deluged.pid')
    if is_daemon_running(pid_file):
        print(('Cannot run multiple daemons using the same config directory.\n'
              'If you believe this is an error, you can force a start by deleting: %s' % pid_file))
        sys.exit(1)

    log = getLogger(__name__)

    # If no logfile specified add logging to default location (as well as stdout)
    if not options.logfile:
        options.logfile = get_config_dir('deluged.log')
        file_handler = FileHandler(options.logfile)
        log.addHandler(file_handler)

    def run_daemon(options):
        try:
            from deluge.core.daemon import Daemon
            daemon = Daemon(listen_interface=options.listen_interface,
                            interface=options.ui_interface,
                            port=options.port,
                            read_only_config_keys=options.read_only_config_keys.split(','))
            if skip_start:
                return daemon
            else:
                daemon.start()

        except Exception as ex:
            log.exception(ex)
            sys.exit(1)
        finally:
            if options.pidfile:
                os.remove(options.pidfile)

    return run_profiled(run_daemon, options, output_file=options.profile, do_profile=options.profile)
