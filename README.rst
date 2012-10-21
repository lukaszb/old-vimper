
vimper
======

vimper is super simple set of vim plugins. It should work properly on both OSX
(preferably with macvim_) and Linux based systems.

Installation
------------

Simply clone vimper repository somewhere and run::

    $ python bootstrap.py

This would backup existing vim files installation and create links to the
vimper's repository.

Want an one liner?

    git clone git://github.com/lukaszb/vimper.git ~/.vimper && cd ~/.vimper && python bootstrap.py


Configuration
-------------

You may want to configure some parts of your vim, i.e. default background style
or directory path where nerd tree should open by default. Guess what? It's
extremely easy to accomplish!

There are 4 files that might be created for that:

- *.vimrc.before* - configuration file loaded before vimper's *.vimrc*
- *.vimrc.local* - confiuration file loaded after vimper's *.vimrc*
- *.gvimrc.before* - as above but for gui vim
- *.gvimrc.local* - as above but for gui vim

So, let's say you want to change default NERDTree path and set background style
to *light*:

    $ cat - > .gvimrc.before
    set bg=light
    let GUI_NERDTREE_DEFAULT_PATH="~/develop/workspace/"

It needs to be *.gvimrc.before* as *GUI_NERDTREE_DEFAULT_PATH* is checked
during *.gvimrc* configuration.

.. _macvim: http://code.google.com/p/macvim/

