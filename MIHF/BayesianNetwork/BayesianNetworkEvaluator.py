import Evaluator
from io import StringIO
import numpy as np
import sys


class BayesianNetworkEvaluator(Evaluator.Evaluator):
    def __init__(self, details):
        pass

    def evaluate(self, input_str, target_output, output, log):
        try:
            if not output:
                raise ValueError("Received empty output. This could be caused by the execution "
                                 "exceeding the given time limit.")
            target_output_values = [float(value) for value in target_output.strip().split('\n')]
            output_values = [float(value) for value in output.strip().split('\n')]
            if len(target_output_values) != len(output_values):
                return (0, "Expected {0} probability values but received {1}.\n\noutput:\n\n{2}\n\nexpected output:\n\n"
                           "{3}\n\nfirst 10k chars of input:\n\n{4}".format(
                    str(len(target_output_values)), str(len(output_values)), output, target_output, input_str
                ))
            for target, current_output in zip(target_output_values, output_values):
                if abs(target - current_output) > 0.0001:
                    return (0, "One or more probabilities exceeded the 0.0001 error treshold for "
                               "target output:\n\n{1}\n\nactual output:\n\n{2}\n\nfirst 10k chars of input:\n\n{0}".format(
                        input_str, target_output, output
                    ))
            return (1, "")
        except (ValueError, OverflowError) as err:
            return (0, "{0}\nfor input:\n\n {1}".format(err.message, input_str))
        except:
            print sys.exc_info()[0]
            return (0, "Unknown error:\n {0} \nfor input:\n\n {1}".format(sys.exc_info()[0], input_str))
