import os

from .twisted.trial import unittest

from deluge.common import (VersionSplit, fdate, fpcnt, fpeer, fsize, fspeed, ftime, get_path_size, is_infohash, is_ip,
                           is_magnet, is_url)
from deluge.ui.util import lang


class CommonTestCase(unittest.TestCase):
    def setUp(self):  # NOQA
        lang.setup_translations()

    def tearDown(self):  # NOQA
        pass

    def test_fsize(self):
        self.assertEqual(fsize(0), '0 B')
        self.assertEqual(fsize(100), '100 B')
        self.assertEqual(fsize(1023), '1023 B')
        self.assertEqual(fsize(1024), '1.0 KiB')
        self.assertEqual(fsize(1048575), '1024.0 KiB')
        self.assertEqual(fsize(1048576), '1.0 MiB')
        self.assertEqual(fsize(1073741823), '1024.0 MiB')
        self.assertEqual(fsize(1073741824), '1.0 GiB')
        self.assertEqual(fsize(112245), '109.6 KiB')
        self.assertEqual(fsize(110723441824), '103.1 GiB')
        self.assertEqual(fsize(1099511627775), '1024.0 GiB')
        self.assertEqual(fsize(1099511627777), '1.0 TiB')
        self.assertEqual(fsize(766148267453245), '696.8 TiB')

    def test_fpcnt(self):
        self.assertTrue(fpcnt(0.9311) == '93.11%')

    def test_fspeed(self):
        self.assertTrue(fspeed(43134) == '42.1 KiB/s')

    def test_fpeer(self):
        self.assertTrue(fpeer(10, 20) == '10 (20)')
        self.assertTrue(fpeer(10, -1) == '10')

    def test_ftime(self):
        self.assertTrue(ftime(0) == '')
        self.assertTrue(ftime(5) == '5s')
        self.assertTrue(ftime(100) == '1m 40s')
        self.assertTrue(ftime(3789) == '1h 3m')
        self.assertTrue(ftime(23011) == '6h 23m')
        self.assertTrue(ftime(391187) == '4d 12h')
        self.assertTrue(ftime(604800) == '1w 0d')
        self.assertTrue(ftime(13893086) == '22w 6d')
        self.assertTrue(ftime(59740269) == '1y 46w')

    def test_fdate(self):
        self.assertTrue(fdate(-1) == '')

    def test_is_url(self):
        self.assertTrue(is_url('http://deluge-torrent.org'))
        self.assertFalse(is_url('file://test.torrent'))

    def test_is_magnet(self):
        self.assertTrue(is_magnet('magnet:?xt=urn:btih:SU5225URMTUEQLDXQWRB2EQWN6KLTYKN'))

    def test_is_infohash(self):
        self.assertTrue(is_infohash('2dc5d0e71a66fe69649a640d39cb00a259704973'))

    def test_get_path_size(self):
        self.assertTrue(get_path_size(os.devnull) == 0)
        self.assertTrue(get_path_size('non-existant.file') == -1)

    def test_is_ip(self):
        self.assertTrue(is_ip('127.0.0.1'))
        self.assertFalse(is_ip('127..0.0'))

    def test_version_split(self):
        self.assertTrue(VersionSplit('1.2.2') == VersionSplit('1.2.2'))
        self.assertTrue(VersionSplit('1.2.1') < VersionSplit('1.2.2'))
        self.assertTrue(VersionSplit('1.1.9') < VersionSplit('1.2.2'))
        self.assertTrue(VersionSplit('1.2.2') > VersionSplit('1.2.1'))
        self.assertTrue(VersionSplit('1.2.2') < VersionSplit('1.2.2-dev'))
        self.assertTrue(VersionSplit('1.2.2-dev') < VersionSplit('1.3.0-rc2'))
        self.assertTrue(VersionSplit('1.2.2') > VersionSplit('1.2.2-rc2'))
        self.assertTrue(VersionSplit('1.2.2-rc2-dev') > VersionSplit('1.2.2-rc2'))
        self.assertTrue(VersionSplit('1.2.2-rc3') > VersionSplit('1.2.2-rc2'))
        self.assertTrue(VersionSplit('0.14.9') == VersionSplit('0.14.9'))
        self.assertTrue(VersionSplit('0.14.9') > VersionSplit('0.14.5'))
        self.assertTrue(VersionSplit('0.14.10') >= VersionSplit('0.14.9'))
        self.assertTrue(VersionSplit('1.4.0') > VersionSplit('1.3.900.dev123'))
        self.assertTrue(VersionSplit('1.3.2rc2.dev1') < VersionSplit('1.3.2-rc2'))
        self.assertTrue(VersionSplit('1.3.900.dev888') > VersionSplit('1.3.900.dev123'))
        self.assertTrue(VersionSplit('1.4.0') > VersionSplit('1.4.0.dev123'))
        self.assertTrue(VersionSplit('1.4.0.dev1') < VersionSplit('1.4.0'))
        self.assertTrue(VersionSplit('1.4.0a1') < VersionSplit('1.4.0'))

    def test_parse_human_size(self):
        from deluge.common import parse_human_size
        sizes = [('1', 1),
                 ('10 bytes', 10),
                 ('2048 bytes', 2048),
                 ('1MiB', 2**(10 * 2)),
                 ('1 MiB', 2**(10 * 2)),
                 ('1 GiB', 2**(10 * 3)),
                 ('1 GiB', 2**(10 * 3)),
                 ('1M', 10**6),
                 ('1MB', 10**6),
                 ('1 GB', 10**9),
                 ('1 TB', 10**12)]

        for human_size, byte_size in sizes:
            parsed = parse_human_size(human_size)
            self.assertEqual(parsed, byte_size, "Mismatch when converting '%s'" % human_size)
