import fastapi

import src.api.routes.admin.authority.user
import src.api.routes.admin.authority.role
import src.api.routes.admin.authority.permission
import src.api.routes.admin.embeddings.collection
import src.api.routes.admin.embeddings.source
import src.api.routes.admin.embeddings.document
import src.api.routes.admin.embeddings.app

import src.api.routes.api.authentication
import src.api.routes.api.user
import src.api.routes.api.embeddings

router = fastapi.APIRouter()

# admin
router.include_router(router=src.api.routes.admin.authority.user.router)
router.include_router(router=src.api.routes.admin.authority.role.router)
router.include_router(router=src.api.routes.admin.authority.permission.router)
router.include_router(router=src.api.routes.admin.embeddings.collection.router)
router.include_router(router=src.api.routes.admin.embeddings.source.router)
router.include_router(router=src.api.routes.admin.embeddings.document.router)
router.include_router(router=src.api.routes.admin.embeddings.app.router)

# api
router.include_router(router=src.api.routes.api.authentication.router)
router.include_router(router=src.api.routes.api.user.router)
router.include_router(router=src.api.routes.api.embeddings.router)
