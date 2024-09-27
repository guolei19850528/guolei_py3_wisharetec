# guolei-py3-wisharetec

### a python3 library for wisharetec

# Example

```python
import diskcache
from guolei_py3_wisharetec.library.scaasp.admin.api import (
    Api as ScaaspAdminApi,
    ApiUrlSettings as ScaaspAdminApiUrlSettings
)

sccaasp_admin_api = ScaaspAdminApi(
    base_url="<BASE_URL>",
    username="<USERNAME>",
    password="<PASSWORD>",
    cache_instance=diskcache.Cache()
)

result = sccaasp_admin_api.login().get(
    url="<URL>",
    params={},
    kwargs={},
    custom_callable=None
)

```