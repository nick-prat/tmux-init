# TMUX-INIT
Start yaml-scripted tmux environments easily

tmux-init will use `/.tmux-init.yml` to generate the session

The supported options are as follows:
```yaml
session-name: <session name>
windows:
  - name: <window name>
    path: <relative path to directory>
```

tmux-init can also read from your `~/.tmux-init.yml` for a list of saved projects!

for example, if you had
```yaml
projects:
  - name: foobar
    path: /path/too/foobar
```

the command `tmux-init -p foobar` would use `/path/too/foobar/.tmux-init.yml` to generate the session.
