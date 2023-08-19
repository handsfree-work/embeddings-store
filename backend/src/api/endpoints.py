import fastapi

import src.api.routes.admin.authority.user
import src.api.routes.admin.authority.role
import src.api.routes.admin.authority.permission

import src.api.routes.api.authentication
import src.api.routes.api.user
import src.api.routes.api.embeddings.em_controller

router = fastapi.APIRouter()

# admin
router.include_router(router=src.api.routes.admin.authority.user.router)
router.include_router(router=src.api.routes.admin.authority.role.router)
router.include_router(router=src.api.routes.admin.authority.permission.router)

# api
router.include_router(router=src.api.routes.api.authentication.router)
router.include_router(router=src.api.routes.api.user.router)
router.include_router(router=src.api.routes.api.embeddings.em_controller.router)
