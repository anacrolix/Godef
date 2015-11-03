import sublime
import sublime_plugin
import subprocess
import os
import platform
import sys


class GodefCommand(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.active_view()
        settings = view.settings()
        godefpath = settings.get('godef', 'godef')
        env = os.environ.copy()
        env.update(filter(lambda x: x[0] == 'GOPATH', settings.get('env').items()))
        # print(env)
        filename = view.file_name()
        select = view.sel()[0]
        select_begin = select.begin()
        select_before = sublime.Region(0, select_begin)
        string_before = view.substr(select_before)
        string_before.encode("utf-8")
        buffer_before = bytearray(string_before, encoding="utf8")
        offset = len(buffer_before)
        print("[Godef]INFO: selcet_begin: %s offset: %s" %
              (str(select_begin), str(offset)))
        args = [godefpath, "-f", filename, "-o", str(offset)]
        print("[Godef]INFO: spawning: %s" % " ".join(args))

        p = subprocess.Popen(args, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, env=env)
        output, stderr = p.communicate()
        if stderr:
            print(stderr)
            return

        location = output.decode("utf-8").rstrip().rsplit(":", 2)
        if len(location) == 3:
            print("[Godef]INFO: godef output: %s" % str(output))
            file = location[0]
            row = int(location[1])
            col = int(location[2])

            position = file + ":" + str(row) + ":" + str(col)
            print("[Godef]INFO: opening definition at %s" % position)
            view = self.window.open_file(position, sublime.ENCODED_POSITION)
        else:
            print("[Godef]ERROR: godef output bad: %s" % str(output))
        print("=================[Godef] End =================")
