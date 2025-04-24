current_dir = $(shell pwd)

install:
	unlink ~/.local/bin/tmux-init 
	ln -s $(current_dir)/src/tmux_init.py ~/.local/bin/tmux-init