import multiprocessing.pool


# Diff support class, useful to make processes No-Daemonic and to ensure that, when I create new processes, they can in turn create other ones
class NoDeamonPool(multiprocessing.pool.Pool):
    def Process(self, *args, **kwds):
        proc = super(NoDeamonPool, self).Process(*args, **kwds)

        class NonDaemonProcess(proc.__class__):
            """Monkey-patch process to ensure it is never daemonized"""
            @property
            def daemon(self):
                return False

            @daemon.setter
            def daemon(self, val):
                pass

        proc.__class__ = NonDaemonProcess
        return proc