import os
import unittest

from diskcache import Cache

diskcache_cache_default = Cache(
    directory=os.path.join(os.path.dirname(__file__), "runtime", "cache", "diskcache", "default"),
)
# os.makedirs(os.path.join(os.path.dirname(__file__), "runtime", "download", "aaa"),exist_ok=True)
from guolei_py3_wisharetec.v1.scaasp.admin.api import Api as WisharetecScaaspAdminApi


class MyTestCase(unittest.TestCase):
    def test_something(self):
        wisharetec_scaasp_admin_api = WisharetecScaaspAdminApi(
            base_url="https://sq.wisharetec.com/",
            diskcache_cache=diskcache_cache_default
        )
        business_order_export_id=wisharetec_scaasp_admin_api.login_with_cache().business_order_export(types=1,request_func_kwargs={
            "params":{
                "orderType":1,
                "subHandle":1,
                "orderStatus":4,
                "shopId":"aae02140-ce1d-11ee-9d82-08c0ebf56c4a"
            }
        })
        # print(business_order_export_id)
        # print(os.path.dirname(os.path.join(os.path.dirname(__file__), "runtime", "download","ii", "ccc")))
        download_file_path=wisharetec_scaasp_admin_api.login_with_cache().download_export_file(
            export_id=98107,
            download_file_path=os.path.join(os.path.dirname(__file__), "runtime", "download","ii", "ccc"),
        )
        self.assertTrue(True, "Test Failed")  # add assertion here


if __name__ == '__main__':
    unittest.main()
