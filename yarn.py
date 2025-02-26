import os, platform, subprocess, dotbot

class Yarn(dotbot.Plugin):
    _yarnDirective = "yarn"

    def can_handle(self, directive):
        return directive in (self._yarnDirective)

    def handle(self, directive, data):
        if directive == self._yarnDirective:
            return self._process_data("yarn global add", data)
        raise ValueError('yarn cannot handle directive %s' % directive)

    def _process_data(self, install_cmd, data):
        success = self._install(install_cmd, data)
        if success:
            self._log.info('All packages have been installed')
        else:
            self._log.error('Some packages were not installed')
        return success

    def _install(self, install_cmd, packages_list):
        cwd = self._context.base_directory()
        log = self._log
        with open(os.devnull, 'w') as devnull:
            stdin = stdout = stderr = devnull
            for package in packages_list:
                # isInstalled = subprocess.call(cmd, shell=True, stdin=stdin, stdout=stdout, stderr=stderr, cwd=cwd)
                # if isInstalled != 0:
                log.info("Installing %s" % package)
                cmd = "%s %s" % (install_cmd, package)
                result = subprocess.call(cmd, shell=True, stdin=stdin, stdout=stdout, stderr=stderr, cwd=cwd)
                if result != 0:
                    log.warning('Failed to install [%s]' % package)
                    return False
            return True

    def _bootstrap(self, cmd):
        with open(os.devnull, 'w') as devnull:
            stdin = stdout = stderr = devnull
            subprocess.call(cmd, shell=True, stdin=stdin, stdout=stdout, stderr=stderr,
                            cwd=self._context.base_directory())

