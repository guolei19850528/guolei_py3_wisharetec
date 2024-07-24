import os
import unittest

from diskcache import Cache

from guolei_py3_wisharetec.scaasp_v1 import AdminApi as GuoleiPy3WisharetecScaaspV1AdminApi, \
    RequestsResponseCallable as GuoleiPy3WisharetecScaaspV1AdminApiRequestsResponseCallable

diskcache_default_instance = Cache(
    directory=os.path.join(os.path.dirname(__file__), "runtime", "cache", "diskcache", "default"),
)


class MyTestCase(unittest.TestCase):
    def test_something(self):

        self.assertTrue(True, "Test Failed")  # add assertion here


if __name__ == '__main__':
    unittest.main()
