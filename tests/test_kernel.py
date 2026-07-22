import json
import os
import unittest

from egison_kernel.kernel import EgisonKernel, MAX_INLINE_REPL_BYTES


class RecordingWrapper:
    def __init__(self):
        self.commands = []
        self.loaded_source = None
        self.loaded_path = None

    def run_command(self, command, timeout=None):
        self.commands.append((command, timeout))
        if command.startswith('loadFile '):
            self.loaded_path = json.loads(command[len('loadFile '):])
            with open(self.loaded_path, encoding='utf-8') as source_file:
                self.loaded_source = source_file.read()
        return 'output'


def kernel_with(wrapper):
    kernel = object.__new__(EgisonKernel)
    kernel.egisonwrapper = wrapper
    return kernel


class RunExpressionTest(unittest.TestCase):
    def test_short_multiline_expression_uses_newline_escape(self):
        wrapper = RecordingWrapper()

        output = kernel_with(wrapper)._run_expression('def x :=\n  42')

        self.assertEqual(output, 'output')
        self.assertEqual(wrapper.commands, [('def x :=#newline  42', None)])

    def test_large_expression_is_loaded_from_temporary_file(self):
        wrapper = RecordingWrapper()
        expression = 'def longValue := "' + ('あ' * MAX_INLINE_REPL_BYTES) + '"'

        output = kernel_with(wrapper)._run_expression(expression)

        self.assertEqual(output, 'output')
        self.assertTrue(wrapper.commands[0][0].startswith('loadFile '))
        self.assertEqual(wrapper.loaded_source, expression + '\n')
        self.assertFalse(os.path.exists(wrapper.loaded_path))


if __name__ == '__main__':
    unittest.main()
