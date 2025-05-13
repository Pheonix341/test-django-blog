from ninja import NinjaAPI

from .faqs import router as faqs_router
from .sliders import router as slider_router
from .categories import router as categories_router
from .articles import router as articles_router
from .auth import router as auth_router
from .users import router as users_router
api = NinjaAPI(
    title='Proweb Blog API',
)

api.add_router('/v1/', faqs_router)
api.add_router('/v1/', slider_router)
api.add_router('/v1/', categories_router)
api.add_router('/v1/', articles_router)
api.add_router('/v1/', auth_router)
api.add_router('/v1/', users_router)


