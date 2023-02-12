import typing

from app.store.crm.accessor import CrmAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_accessors(app: "Application"):
    app.crm_accessor = CrmAccessor()
    app.on_startup.append(app.crm_accessor.connect) # при старте приложения нужно выполнить метод crm_accessor
    app.on_cleanup.append(app.crm_accessor.disconnect) # при моменте чистки приложения
