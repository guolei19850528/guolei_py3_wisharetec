# guolei-py3-wisharetec

### a python3 library for wisharetec

# Example

```python
import diskcache
from guolei_py3_wisharetec.library.scaasp.admin.api import (
    Api as ScaaspAdminApi, UrlSetting as ScaaspAdminApiUrlSetting
)

scaasp_admin_api = ScaaspAdminApi(
    base_url="<BASE URL>",
    username="<USERNAME>",
    password="<PASSWORD>",
    cache_instance=diskcache.Cache()
)

community_by_paginator = scaasp_admin_api.login().get(
    path=ScaaspAdminApiUrlSetting.QUERY_COMMUNITY_BY_PAGINATOR,
    params={
        "curPage": 1,
        "pageSize": 20
    }
)

```