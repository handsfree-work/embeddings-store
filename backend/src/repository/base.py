import src.modules.account.models.db.user
import src.modules.account.models.db.role
import src.modules.account.models.db.user_role
import src.modules.account.models.db.role_permission
import src.modules.account.models.db.permission
from src.modules.embeddings.models.db.index import embeddings_index

import loguru
loguru.logger.debug(embeddings_index)

from src.repository.table import Base
