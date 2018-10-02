import Evaluator
from io import StringIO
import numpy as np
import traceback

class RecommendationSystemEvaluator(Evaluator.Evaluator):
    def __init__(self, details):
        pass

    def evaluate(self, input, target_output, output, log):
        try:
        
            hits = 5
            print 'Started RecommendationSystemEvaluator, output recieved:', output[0:min(len(output),50)]
            #striofile = StringIO(unicode(output), "utf-8")
            
            striofile = StringIO(unicode(output), newline = u'\n')
            print 'Striofile created succesfully'
            res = np.loadtxt(striofile,delimiter="\t",dtype=np.int32)
            print 'If you can read this then text loaded correctly, dimensions of striofile:',res.shape
            R = input['R']*(1-input['miss'])
            perf = 0
            for i in range(input['I']):
                top = set(np.argsort(-R[i,:])[:hits])
                if len(top.intersection(res[i][:hits]))>0:
                    perf += 1
            perf = (perf/float(input['I']))
            print "Performance of this evaluator:",perf
            #score = min(input["missingness"], perf)/float(input['missingness'])
            score = perf/float(input['missingness'])
            return (score, 'Performance = %f, required approximately %f, resulting score = %f'%(perf,input['missingness'],score))
        
        except ValueError as err:
            print err.message
            print (err)
            traceback.print_exc()

            #raise err
            return (0, err.message)
        except:
            return (0, "Unknown error")
