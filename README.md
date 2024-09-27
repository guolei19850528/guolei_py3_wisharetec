# guolei-py3-wisharetec

### a python3 library for wisharetec

# Example

```python
import diskcache
from guolei_py3_wisharetec.library.scaasp.admin.api import Api as AdminApi, ApiUrlSettings as AdminApiUrlSettings

admin_api = AdminApi(
    base_url="<BASE_URL>",
    username="<USERNAME>",
    password="<PASSWORD>",
    cache_instance=diskcache.Cache()
)

result = admin_api.login().get(
    url="<URL>",
    params={},
    kwargs={},
    custom_callable=None
)

```