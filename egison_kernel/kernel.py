# coding: utf-8

# ===== DEFINITIONS =====

from ipykernel.kernelbase import Kernel
from pexpect import replwrap, EOF
from subprocess import check_output
from builtins import str as text

import re
import signal
import uuid

__version__ = '0.1.0'

version_pat = re.compile(r'(\d+(\.\d+)+)')
crlf_pat = re.compile(r'[\r\n]+')


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
                     'mimetype': 'text/plain',
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

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        code = crlf_pat.sub('#newline', code.strip())
        if not code:
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

        interrupted = False
        try:
            output = self.egisonwrapper.run_command(code, timeout=None)
        except KeyboardInterrupt:
            self.egisonwrapper.child.sendintr()
            interrupted = True
            self.egisonwrapper._expect_prompt()
            output = self.egisonwrapper.child.before
        except EOF:
            output = self.egisonwrapper.child.before + 'Restarting Egison'
            self._start_egison()

        if not silent:
            moutput = re.match(r'\#latex\|(.*)\|\#', output)
            if moutput:
                content = {'execution_count': self.execution_count, 'data': {'text/html': u'{}'.format(u'$$' + moutput.group(1) + u'$$')}, 'metadata': {}}
                self.send_response(self.iopub_socket, 'display_data', content)
            else:
                stream_content = {'execution_count': self.execution_count, 'name': 'stdout', 'text': output}
                self.send_response(self.iopub_socket, 'stream', stream_content)

        if interrupted:
            return {'status': 'abort', 'execution_count': self.execution_count}

        return {'status': 'ok', 'execution_count': self.execution_count,
                'payload': [], 'user_expressions': {}}


# ===== MAIN =====
if __name__ == '__main__':
    from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=EgisonKernel)
