import sys
import traceback
import time


class TestLoader(object):
    '''用来识别test_开头的用例，返回一个TestSuite'''

    testMethodPrefix = 'test_'

    #从类中提取prefix(默认是test_)开头的方法名字
    def getTestCaseNames(self, testCaseClass):
        # def isTestMethod(attrname, testCaseClass=testCaseClass,
        #                  prefix=self.testMethodPrefix):
        #     return attrname.startswith(prefix) and \
        #         hasattr(getattr(testCaseClass, attrname), '__call__')
        # testFnNames = list(filter(isTestMethod, dir(testCaseClass)))
        # testFnNames.sort()
        # return testFnNames

        testNames = []
        for name in dir(testCaseClass):
            if name.startswith(self.testMethodPrefix) and hasattr(getattr(testCaseClass, name), '__call__'):
                testNames.append(name)
        return testNames

    #遍历测试类的属性，找到测试方法并组合为一个testsuite
    def loadTestsFromTestClass(self, testCaseClass):
        """Return a suite of all tests cases contained in testCaseClass"""
        testCaseNames = self.getTestCaseNames(testCaseClass)
        testSuite = TestSuite(map(testCaseClass, testCaseNames))
        #map(testCaseClass, testCaseNames) 相当于调用testCaseClass(testCaseName)生成一个TestCase类，__init__定义在基类TestCase中
        return testSuite

    #遍历模块，找TestCase子类并加载到testsuite中
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

    # @classmethod
    # def setUpClass(cls):
    #     "Hook method for setting up class fixture before running tests in the class."

    # @classmethod
    # def tearDownClass(cls):
    #     "Hook method for deconstructing the class fixture after running all tests in the class."

    def id(self):
        return "%s.%s" % (self.__class__, self._testMethodName)

    def __str__(self):
        return "%s (%s)" % (self._testMethodName, self.__class__)

    def __repr__(self):
        return "<%s testMethod=%s>" % (self.__class__, self._testMethodName)

    def countTestCases(self):
        return 1

    def run(self, result):
        result.startTest(self)

        testMethod = getattr(self, self._testMethodName)
       
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
            result.printStatus(success)

        result.finishTest(self)


class TestResult(object):
    def __init__(self, stream=None, descriptions=None, verbosity=None):
        self.success = []
        self.failures = []
        self.errors = []
        self.testsRun = 0

    #在所有测试开始前运行且只运行一次
    def startTestRun(self):
        self.startTime = time.time()
    
    #在所有测试结束后运行且只运行一次
    def finishTestRun(self):
        self.stopTime = time.time()

    #在每个测试开始前运行
    def startTest(self, test):
        self.testsRun += 1

        print('='*80)
        print(f'run: {test}')

    #在每个测试结束后运行
    def finishTest(self, test):
        pass

    def printStatus(self, success):
        status = 'SUCCESS' if success else 'FAIL'            
        print('-'*20)
        print(f'= RESULT: {status} =')

    def addError(self, test, err):
        self.errors.append((test, err))

    def addFailure(self, test, err):
        self.failures.append((test, err))

    def addSuccess(self, test):
        self.success.append(test)

    def _exc_info_to_string(self, err):
        """Converts a sys.exc_info()-style tuple of values into a string."""
        exctype, value, tb = err
        msgLines = traceback.format_exception(exctype, value, tb)
        return ''.join(msgLines)

    def printErrors(self):
        print('='*80)
        for test, err in self.errors:
            print(f'{test}')
            print('-'*80)
            print(self._exc_info_to_string(err))
        for test, err in self.failures:
            print(f'{test}')
            print('-'*80)
            print(self._exc_info_to_string(err))

    def summary(self):
        timeTaken = self.stopTime - self.startTime
        print('='*80)
        print(f'run {self.testsRun} tests in {timeTaken:.2f} secondes, success:{len(self.success)} fail:{len(self.failures)} error:{len(self.errors)}')


class TestRunner(object):
    def run(self, test):
        result = TestResult()
        result.startTestRun()
        test.run(result)
        result.finishTestRun()

        result.printErrors()
        result.summary()
