#!/usr/bin/env python3

import libtmux
import yaml
import argparse
import os

class Project:
    def __init__(self, data):
        self.name = data["name"]
        self.path = data["path"]
    
    def get_path(self):
        return self.path
    
    def get_name(self):
        return self.name
    
    def __str__(self):
        return f"{self.name}: {self.path}"

class Config:
    def __init__(self):
        self.projects = {}

        path = os.path.expanduser("~/.tmux-init.yml")

        if os.path.isfile(path):
            with open(path, "r") as cfg:
                data = yaml.safe_load(cfg)
                for project in data["projects"]:
                    self.add_project(project)
    
    def has_project(self, name) -> bool:
        return name in self.projects
    
    def add_project(self, project) -> None:
        if project["name"] in self.projects:
            raise Exception("duplicate projects")

        self.projects[project["name"]] = Project(project)
    
    def get_project(self, name) -> Project | None:
        return self.projects.get(name, None)
    
    def get_projects(self) -> list[Project]:
        return list(self.projects.values())

def create_session(base_path, recreate, no_attach):
    base_path = os.path.expanduser(base_path)
    path = os.path.join(base_path, ".tmux-init.yml")

    with open(path, "r") as cfg:
        data = yaml.safe_load(cfg)

    server = libtmux.Server()
    session_name = data["session-name"]

    if server.has_session(session_name):
        if recreate:
            server.kill_session(session_name)
        else:
            if not no_attach:
                server.attach_session(session_name)
            exit()

    create_session = True
    for window in data["windows"]:
        start_directory = os.path.join(base_path, window["path"])
        if create_session:
            session = server.new_session(session_name=session_name, attach=False, window_name=window["name"], start_directory=start_directory)
            create_session = False
        else:
            session.new_window(window_name=window["name"], start_directory=start_directory)

    if not no_attach:
        server.attach_session(session.name)

def main():
    parser = argparse.ArgumentParser(prog="tmux-init")
    parser.add_argument("-r", "--recreate", action="store_true", help="If session already exists, replace it")
    parser.add_argument("-f", "--config-file", default=".tmux-init.yml", help="Config file to use to create session")
    parser.add_argument("-n", "--no-attach", action="store_true", help="Create session without attaching")
    parser.add_argument("-p", "--project", help="Load a global project")
    args = parser.parse_args()

    cfg = Config()

    if args.project and not cfg.has_project(args.project):
        raise Exception("project doesn't exist")
    
    project = cfg.get_project(args.project) if args.project else None
    base_path = project.get_path() if project else "."
    create_session(base_path, args.recreate, args.no_attach)


if __name__ == "__main__":
    main()
