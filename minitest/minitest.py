import sys
import traceback
import time


class TestLoader(object):
    '''用来识别test_开头的用例，返回一个TestSuite'''

    testMethodPrefix = 'test'

    def getTestCaseNames(self, testCaseClass):
        """Return a sorted sequence of method names found within testCaseClass
        """
        def isTestMethod(attrname, testCaseClass=testCaseClass,
                         prefix=self.testMethodPrefix):
            return attrname.startswith(prefix) and \
                hasattr(getattr(testCaseClass, attrname), '__call__')
        testFnNames = list(filter(isTestMethod, dir(testCaseClass)))
        testFnNames.sort()
        return testFnNames

    def loadTestsFromTestClass(self, testCaseClass):
        """Return a suite of all tests cases contained in testCaseClass"""
        testCaseNames = self.getTestCaseNames(testCaseClass)
        testSuite = TestSuite(map(testCaseClass, testCaseNames))
        #map(testCaseClass, testCaseNames) 相当于调用testCaseClass(testCaseName)生成一个TestCase类，__init__定义在基类TestCase中
        return testSuite

    def loadTestsFromModule(self, module, use_load_tests=True):
        """Return a suite of all tests cases contained in the given module"""
        tests = []
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, TestCase):
                tests.append(self.loadTestsFromTestClass(obj))

        return TestSuite(tests)

defaultTestLoader = TestLoader()


class TestSuite(object):
    '''组合模式，包含TestCase和TestSuite'''

    def __init__(self, tests):
        self.tests = []
        self.addTests(tests)

    def __repr__(self):
        return "<%s tests=%s>" % (self.__class__, list(self))

    def __iter__(self):
        return iter(self.tests)
    
    def addTests(self, tests):
        for test in tests:
            self.addTest(test)
    
    def addTest(self, test):
        self.tests.append(test)

    def countTestCases(self):
        count = 0
        for test in self:
            count += test.countTestCases()
        return count

    def run(self, result):
        for test in self:
            test.run(result)
        return result


class TestCase(object):

    _classSetuped = False

    def __init__(self, methodName):
        """Create an instance of the class that will use the named test
           method when executed. Raises a ValueError if the instance does
           not have a method with the specified name.
        """
        self._testMethodName = methodName
        try:
            testMethod = getattr(self, methodName)
        except AttributeError:
            raise ValueError("no such test method in %s: %s" %
                  (self.__class__, methodName))
        self._testMethodDoc = testMethod.__doc__

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        pass

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        pass

    @classmethod
    def setUpClass(cls):
        "Hook method for setting up class fixture before running tests in the class."

    @classmethod
    def tearDownClass(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class."

    def getDescription(self):
        """Returns a one-line description of the test, or None if no
        description has been provided.

        The default implementation of this method returns the first line of
        the specified test method's docstring.
        """
        return self._testMethodDoc

    def id(self):
        return "%s.%s" % (self.__class__, self._testMethodName)

    def __str__(self):
        return "%s (%s)" % (self._testMethodName, self.__class__)

    def __repr__(self):
        return "<%s testMethod=%s>" % \
               (self.__class__, self._testMethodName)

    def countTestCases(self):
        return 1

    def run(self, result):
        result.startTest(self)

        testMethod = getattr(self, self._testMethodName)
       
        try:
            success = False
            try:                    
                self.setUp()
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, sys.exc_info())
            else:
                try:
                    testMethod()
                except KeyboardInterrupt:
                    raise
                except:
                    result.addFailure(self, sys.exc_info())
                else:
                    result.addSuccess(self)
                    success = True

                try:
                    self.tearDown()
                except KeyboardInterrupt:
                    raise
                except:
                    result.addError(self, sys.exc_info())
                    success = False

        finally:
            result.stopTest(self)


class TestResult(object):
    def __init__(self, stream=None, descriptions=None, verbosity=None):
        self.success = []
        self.failures = []
        self.errors = []
        self.testsRun = 0

    def startTestRun(self):
        self.startTime = time.time()
    
    def stopTestRun(self):
        self.stopTime = time.time()

    def startTest(self, test):
        "Called when the given test is about to be run"
        self.testsRun += 1

        print('='*80)
        print(f'run: {test}')
        print(test.getDescription())

    def stopTest(self, test):
        pass

    def printStatus(self, result):
        print('-'*20)
        print(f'= RESULT: {result} =')
        print('-'*20)

    def addError(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info().
        """
        self.errors.append((test, self._exc_info_to_string(err, test)))
        self.printStatus('ERROR')
        print(self._exc_info_to_string(err, test))

    def addFailure(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info()."""
        self.failures.append((test, self._exc_info_to_string(err, test)))
        self.printStatus('FAIL')
        print(self._exc_info_to_string(err, test))

    def addSuccess(self, test):
        "Called when a test has completed successfully"
        self.success.append(test)
        self.printStatus('SUCCESS')

    def _exc_info_to_string(self, err, test):
        """Converts a sys.exc_info()-style tuple of values into a string."""
        exctype, value, tb = err
        msgLines = traceback.format_exception(exctype, value, tb)
        return ''.join(msgLines) 

    def __repr__(self):
        return ("<%s run=%i errors=%i failures=%i>" %
               (self.__class__, self.testsRun, len(self.errors),
                len(self.failures)))

    def summary(self):
        timeTaken = self.stopTime - self.startTime
        print('='*80)
        print(f'run {self.testsRun} in {timeTaken:.2f} secondes, [success:{len(self.success)} fail:{len(self.failures)} error:{len(self.errors)}]')


class TestRunner(object):

    def run(self, test):
        result = TestResult()
        result.startTestRun()
        test.run(result)
        result.stopTestRun()

        result.summary()
