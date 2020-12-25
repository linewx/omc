import pkg_resources

from omc import utils
from omc.config import settings

from omc.utils import file_utils

from omc.common import CmdTaskMixin
from omc.core import Resource
import os
import stat


class Config(Resource, CmdTaskMixin):
    def init(self):
        # 1. set up omc-completion.sh
        completion_helper = 'omc-completion.sh'
        completion_scripts = pkg_resources.resource_filename(__name__, '../../lib/' + completion_helper)
        file_utils.make_directory(settings.BIN_DIR)
        file_utils.copy(completion_scripts, settings.BIN_DIR)

        # 2. change the file to executable
        the_completion_file_name = os.path.join(settings.BIN_DIR, completion_helper)
        mode = os.stat(the_completion_file_name).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(the_completion_file_name, mode)

        # 3. install omc plugins to omz
        omz_custom = os.path.join(os.environ.get("HOME"), ".oh-my-zsh/custom/plugins")
        omw_plugin_dir = os.path.join(omz_custom, 'omc')
        if os.path.exists(omz_custom):
            file_utils.make_directory(omw_plugin_dir)

            omz_completion_file_ = pkg_resources.resource_filename(__name__, '../../lib/_omc')
            file_utils.copy(omz_completion_file_, omw_plugin_dir)

    def sync_version(self):
        pass
