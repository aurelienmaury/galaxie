#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cmd2 import Cmd

class HelloWorld(Cmd):
    """Simple command processor example."""

    def do_greet(self, line):
        print "hello "+line

    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    HelloWorld().cmdloop()