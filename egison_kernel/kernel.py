# coding: utf-8

# ===== DEFINITIONS =====

from ipykernel.kernelbase import Kernel
from pexpect import replwrap, EOF
from subprocess import check_output
from builtins import str as text

import json
import os
import re
import signal
import tempfile
import uuid

__version__ = '0.1.0'

version_pat = re.compile(r'(\d+(\.\d+)+)')
crlf_pat = re.compile(r'[\r\n]+')

# macOS terminals have a relatively small canonical input buffer.  Keep enough
# headroom for multibyte input and the REPL's own processing.
MAX_INLINE_REPL_BYTES = 768


class EgisonKernel(Kernel):
    implementation = 'egison_kernel'
    implementation_version = __version__

    _language_version = None

    @property
    def language_version(self):
        if self._language_version is None:
            m = version_pat.search(check_output(['egison', '--version']).decode('utf-8'))
            self._language_version = m.group(1)
        return self._language_version

    @property
    def banner(self):
        return u'Simple Egison Kernel (Egison v%s)' % self.language_version

    language_info = {'name': 'egison',
                     'codemirror_mode': 'egison',
                     'mimetype': 'text/x-egison',
                     'file_extension': '.egi'}

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_egison()

    def _start_egison(self):
        # Signal handlers are inherited by forked processes, and we can't easily
        # reset it from the subprocess. Since kernelapp ignores SIGINT except in
        # message handlers, we need to temporarily reset the SIGINT handler here
        # so that Egison is interruptible.
        sig = signal.signal(signal.SIGINT, signal.SIG_DFL)
        prompt = uuid.uuid4().hex + ">"
        try:
            self.egisonwrapper = replwrap.REPLWrapper("egison -M latex --prompt " + prompt,
                                                      text(prompt), None)
        finally:
            signal.signal(signal.SIGINT, sig)

    def _split_expressions(self, code):
        """Split cell code into individual top-level expressions.

        A new expression starts when a non-blank, non-indented line appears.
        Indented lines are continuation of the previous expression.
        """
        expressions = []
        current_lines = []

        for line in code.split('\n'):
            if line.strip() == '':
                # Blank line: include in current expression as separator
                if current_lines:
                    current_lines.append(line)
                continue

            if line[0] != ' ' and line[0] != '\t' and current_lines:
                # Non-indented line with existing expression -> start new expression
                # Remove trailing blank lines from previous expression
                while current_lines and current_lines[-1].strip() == '':
                    current_lines.pop()
                if current_lines:
                    expressions.append('\n'.join(current_lines))
                current_lines = [line]
            else:
                current_lines.append(line)

        # Don't forget the last expression
        while current_lines and current_lines[-1].strip() == '':
            current_lines.pop()
        if current_lines:
            expressions.append('\n'.join(current_lines))

        return expressions

    def _run_expression(self, expr):
        """Run one top-level expression without overflowing the REPL's PTY.

        Egison's ``#newline`` escape lets the kernel submit a multiline
        expression as one REPL line.  A sufficiently large expression exceeds
        the terminal's canonical line limit, however, and the PTY responds with
        BEL characters instead of delivering it to Egison.  Loading a temporary
        source file avoids that limit while evaluating in the same REPL
        environment and preserving normal output.
        """
        repl_code = crlf_pat.sub('#newline', expr)
        if len(repl_code.encode('utf-8')) <= MAX_INLINE_REPL_BYTES:
            return self.egisonwrapper.run_command(repl_code, timeout=None)

        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                    mode='w', suffix='.egi', encoding='utf-8',
                    newline='\n', delete=False) as source_file:
                temp_path = source_file.name
                source_file.write(expr)
                source_file.write('\n')

            command = 'loadFile ' + json.dumps(temp_path, ensure_ascii=False)
            return self.egisonwrapper.run_command(command, timeout=None)
        finally:
            if temp_path is not None:
                try:
                    os.unlink(temp_path)
                except FileNotFoundError:
                    pass

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        code = code.strip()
        if not code:
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

        expressions = self._split_expressions(code)
        interrupted = False

        for expr in expressions:
            try:
                output = self._run_expression(expr)
            except KeyboardInterrupt:
                self.egisonwrapper.child.sendintr()
                interrupted = True
                self.egisonwrapper._expect_prompt()
                output = self.egisonwrapper.child.before
            except EOF:
                output = self.egisonwrapper.child.before + 'Restarting Egison'
                self._start_egison()
                break

            if not silent and output and output.strip():
                moutput = re.match(r'\#latex\|(.*)\|\#', output)
                if moutput:
                    content = {'execution_count': self.execution_count, 'data': {'text/html': u'{}'.format(u'$' + moutput.group(1) + u'$')}, 'metadata': {}}
                    self.send_response(self.iopub_socket, 'display_data', content)
                else:
                    stream_content = {'execution_count': self.execution_count, 'name': 'stdout', 'text': output}
                    self.send_response(self.iopub_socket, 'stream', stream_content)

            if interrupted:
                break

        if interrupted:
            return {'status': 'abort', 'execution_count': self.execution_count}

        return {'status': 'ok', 'execution_count': self.execution_count,
                'payload': [], 'user_expressions': {}}


# ===== MAIN =====
if __name__ == '__main__':
    from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=EgisonKernel)
