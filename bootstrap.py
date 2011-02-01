#!/usr/bin/env python
import os
import sys
import shutil
import datetime
from contrib import logger
from subprocess import Popen, PIPE

abspath = lambda *p: os.path.abspath(os.path.join(*p))
now = datetime.datetime.now()
DATE_FORMAT = '%Y%m%d%H%M%S'

HOME_DIR = os.environ['HOME']
ROOT_DIR = abspath(os.path.dirname(__file__))
BUNDLE_DIR = abspath(ROOT_DIR, 'vim', 'bundle')
RUBY_BIN = '/usr/bin/ruby'

def setup_env():
    if 'VIMPER_RUBY_BIN' in os.environ:
        global RUBY_BIN
        RUBY_BIN = os.environ['VIMPER_RUBY_BIN']


links = (
    (abspath(ROOT_DIR, 'vim'), abspath(HOME_DIR, '.vim')),
    (abspath(ROOT_DIR, 'vim/vimrc'), abspath(HOME_DIR, '.vimrc')),
    (abspath(ROOT_DIR, 'vim/gvimrc'), abspath(HOME_DIR, '.gvimrc')),
)

def redefine_links():
    # Create links and backup if needed
    for src, dst in links:
        if os.path.islink(dst):
            orgpath = os.readlink(dst)
            logger.debug("Found link: %s => %s" % (dst, orgpath))
            os.remove(dst)
            logger.warn("Removed link %s " % dst)
        elif os.path.exists(dst):
            newpath = '%s-%s' % (dst, now.strftime(DATE_FORMAT))
            shutil.move(dst, newpath)
            logger.debug("Moved %s to %s" % (dst, newpath))
        else:
            logger.debug("No entry at %s" % dst)
        os.symlink(src, dst)
        logger.info("Created link %s ==> %s" % (dst, src))


VIM_PLUGINS = {
    'closetag':       'git://github.com/vim-scripts/closetag.vim.git',
    'commandt':       'git://github.com/wincent/Command-T.git',
    'fugitive':       'git://github.com/tpope/vim-fugitive.git',
    'git':            'git://github.com/tpope/vim-git.git',
    'ir_black':       'git://github.com/lukaszb/vim-irblack.git',
    'nerdcommenter':  'git://github.com/scrooloose/nerdcommenter.git',
    'nerdtree':       'git://github.com/scrooloose/nerdtree.git',
    'supertab':       'git://github.com/ervandew/supertab.git',
    'surround':       'git://github.com/tpope/vim-surround.git',
}

# OSX Changes
if sys.platform == 'darwin':
    VIM_PLUGINS['nerdtree'] = 'git://github.com/lukaszb/nerdtree.git'

def run_cmd(cmd, stdout=None, stderr=None, cwd=None, shell=None):
    if stdout is None:
        stdout = sys.stdout
    if stderr is None:
        stderr = sys.stderr
    if shell is None:
        shell = True
    p = Popen(cmd, shell=True, cwd=cwd, stdout=stdout, stderr=stderr)
    return p.communicate()


def get_plugin(name, uri):
    dst = abspath(BUNDLE_DIR, name)

    # Git repo
    if uri.endswith('git'):
        if os.path.isdir(dst) and os.path.isdir(abspath(dst, '.git')):
            # Update git repo (git pull)
            logger.debug("Fetching %s => %s" % (uri, dst))
            run_cmd('git pull origin master', cwd=dst)
        else:
            logger.debug("Cloning %s => %s" % (uri, dst))
            run_cmd('git clone %s %s' % (uri, dst))

def post_actions():
    # Command-T
    COMMANDT_DIR = abspath(BUNDLE_DIR, 'commandt')
    src_dir = abspath(COMMANDT_DIR, 'ruby', 'command-t')
    cmd = '%s extconf.rb' % RUBY_BIN
    run_cmd(cmd, cwd=src_dir, stdout=PIPE, stderr=PIPE)
    run_cmd('make clean && make', cwd=src_dir)


def main():
    # Prepare
    setup_env()
    redefine_links()
    backupdir = abspath(HOME_DIR, '.vim/', 'backup')
    if not os.path.isdir(backupdir):
        os.makedirs(backupdir)
    # Fetch plugins
    for name, uri in VIM_PLUGINS.iteritems():
        get_plugin(name, uri)
    post_actions()

if __name__ == '__main__':
    main()

