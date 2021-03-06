#!/usr/bin/env python2

# THIS FILE IS PART OF THE CYLC SUITE ENGINE.
# Copyright (C) 2008-2019 NIWA & British Crown (Met Office) & Contributors.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from tempfile import NamedTemporaryFile, SpooledTemporaryFile, TemporaryFile
import unittest

from cylc.subprocctx import SubProcContext
from cylc.subprocpool import SubProcPool


class TestSubProcPool(unittest.TestCase):

    def test_get_temporary_file(self):
        """Test SubProcPool.get_temporary_file."""
        self.assertIsInstance(
            SubProcPool.get_temporary_file(), SpooledTemporaryFile)

    def test_run_command_returns_0(self):
        """Test basic usage, command returns 0"""
        ctx = SubProcContext('truth', ['true'])
        SubProcPool.run_command(ctx)
        self.assertEqual(ctx.err, '')
        self.assertEqual(ctx.out, '')
        self.assertEqual(ctx.ret_code, 0)

    def test_run_command_returns_1(self):
        """Test basic usage, command returns 1"""
        ctx = SubProcContext('lies', ['false'])
        SubProcPool.run_command(ctx)
        self.assertEqual(ctx.err, '')
        self.assertEqual(ctx.out, '')
        self.assertEqual(ctx.ret_code, 1)

    def test_run_command_writes_to_out(self):
        """Test basic usage, command writes to STDOUT"""
        ctx = SubProcContext('parrot', ['echo', 'pirate', 'urrrr'])
        SubProcPool.run_command(ctx)
        self.assertEqual(ctx.err, '')
        self.assertEqual(ctx.out, 'pirate urrrr\n')
        self.assertEqual(ctx.ret_code, 0)

    def test_run_command_writes_to_err(self):
        """Test basic usage, command writes to STDERR"""
        ctx = SubProcContext(
            'parrot2', ['bash', '-c', 'echo pirate errrr >&2'])
        SubProcPool.run_command(ctx)
        self.assertEqual(ctx.err, 'pirate errrr\n')
        self.assertEqual(ctx.out, '')
        self.assertEqual(ctx.ret_code, 0)

    def test_run_command_with_stdin_from_str(self):
        """Test STDIN from string"""
        ctx = SubProcContext('meow', ['cat'], stdin_str='catches mice.\n')
        SubProcPool.run_command(ctx)
        self.assertEqual(ctx.err, '')
        self.assertEqual(ctx.out, 'catches mice.\n')
        self.assertEqual(ctx.ret_code, 0)

    def test_run_command_with_stdin_from_unicode(self):
        """Test STDIN from string with Unicode"""
        ctx = SubProcContext('meow', ['cat'], stdin_str='喵\n')
        SubProcPool.run_command(ctx)
        self.assertEqual(ctx.err, '')
        self.assertEqual(ctx.out, '喵\n')
        self.assertEqual(ctx.ret_code, 0)

    def test_run_command_with_stdin_from_handle(self):
        """Test STDIN from a single opened file handle"""
        handle = TemporaryFile()
        handle.write('catches mice.\n'.encode('UTF-8'))
        handle.seek(0)
        ctx = SubProcContext('meow', ['cat'], stdin_files=[handle])
        SubProcPool.run_command(ctx)
        self.assertEqual(ctx.err, '')
        self.assertEqual(ctx.out, 'catches mice.\n')
        self.assertEqual(ctx.ret_code, 0)
        handle.close()

    def test_run_command_with_stdin_from_path(self):
        """Test STDIN from a single file path"""
        handle = NamedTemporaryFile()
        handle.write('catches mice.\n'.encode('UTF-8'))
        handle.seek(0)
        ctx = SubProcContext('meow', ['cat'], stdin_files=[handle.name])
        SubProcPool.run_command(ctx)
        self.assertEqual(ctx.err, '')
        self.assertEqual(ctx.out, 'catches mice.\n')
        self.assertEqual(ctx.ret_code, 0)
        handle.close()

    def test_run_command_with_stdin_from_handles(self):
        """Test STDIN from multiple file handles"""
        handles = []
        for txt in ['catches mice.\n', 'eat fish.\n']:
            handle = TemporaryFile()
            handle.write(txt.encode('UTF-8'))
            handle.seek(0)
            handles.append(handle)
        ctx = SubProcContext('meow', ['cat'], stdin_files=handles)
        SubProcPool.run_command(ctx)
        self.assertEqual(ctx.err, '')
        self.assertEqual(ctx.out, 'catches mice.\neat fish.\n')
        self.assertEqual(ctx.ret_code, 0)
        for handle in handles:
            handle.close()

    def test_run_command_with_stdin_from_paths(self):
        """Test STDIN from multiple file paths"""
        handles = []
        for txt in ['catches mice.\n', 'eat fish.\n']:
            handle = NamedTemporaryFile()
            handle.write(txt.encode('UTF-8'))
            handle.seek(0)
            handles.append(handle)
        ctx = SubProcContext(
            'meow', ['cat'], stdin_files=[handle.name for handle in handles])
        SubProcPool.run_command(ctx)
        self.assertEqual(ctx.err, '')
        self.assertEqual(ctx.out, 'catches mice.\neat fish.\n')
        self.assertEqual(ctx.ret_code, 0)
        for handle in handles:
            handle.close()


if __name__ == '__main__':
    unittest.main()
