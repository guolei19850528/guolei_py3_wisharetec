import os
import unittest

from diskcache import Cache

diskcache_cache_default_instance = Cache(
    directory=os.path.join(os.path.dirname(__file__), "runtime", "cache", "diskcache", "default"),
)

from guolei_py3_wisharetec.v1.scaasp.admin.api import Api as WisharetecScaaspAdminApi


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertTrue(True, "Test Failed")  # add assertion here


if __name__ == '__main__':
    unittest.main()
