import Tester
import json
import time
import numpy as np
from MIHF.Maze.maze_manager import MazeManager

class MazeTester(Tester.Tester):

    def __init__(self, details):
        super(MazeTester, self).__init__(details)

        tests_file = details["tests"]

        with open(tests_file, "r") as data_file:
            self.__tests = json.load(data_file)
        self.__break_on_first_error = details["break on first error"]
        self.__break_on_first_wrong = details["break on first wrong"]
        self.__default_timeout = details.get("default timeout") or 5.0
        pass


    def test(self, project_name, submission):

        tests = self.__tests
        mazeManager = MazeManager()

        for mazeindex,data in enumerate(tests):
            timeout = self.__default_timeout

            inputparams = data["input"]
            timeout = data.get("timeout") or self.__default_timeout

            pr = inputparams.split(",")
            mazeX = int(pr[0])
            mazeY = int(pr[1])
            mazeObjects = int(pr[2])
            
            #Generate a maze
            currentMaze = mazeManager.add_maze(mazeX,mazeY,mazeObjects,mazeindex+1)
            inputstr = mazeManager.print_maze_to_str(mazeindex+1)

            (stdout, stderr, extraerr) = submission.run(project_name, inputstr, timeout = timeout)

            stdout = stdout.decode('utf-8','ignore').encode('ascii','replace').strip()

            eval_inputs = {'mazemanager':mazeManager,'mazeID':mazeindex+1}

            if not (stderr or extraerr):
                (result, message) = self.evaluator.evaluate(eval_inputs, None, stdout, submission.log)
            else:
                result = 0
                if stderr:
                    if len(inputstr)> 10000:
                        message = "Runtime error:\n%s\n\n for TRUNCATED [10000 chars] input:\n%s" % (stderr,inputstr[0:min(10000,len(inputstr))])
                    else:
                        message = "Runtime error:\n%s\n\nfor complete input:\n%s" % (stderr,inputstr[0:min(10000,len(inputstr))])
                else:
                    message = extraerr +'\nstdout was:' + stdout

            submission.log.log_test(project_name, eval_inputs, "", stdout, result, message)

            if self.__break_on_first_error and (stderr or extraerr):
                break

            if self.__break_on_first_wrong and result != 1.0:
                break