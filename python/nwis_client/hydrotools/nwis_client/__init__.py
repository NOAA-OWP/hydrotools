from .iv import IVDataService

# Monkeypatch get classmethod so it's accessable at subpackage level
get = IVDataService.get
