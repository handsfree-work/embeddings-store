from src.modules.account.models.db.index import account_index
from src.modules.embeddings.models.db.index import embeddings_index

import loguru

from src.repository.table import Base

loguru.logger.trace(embeddings_index, account_index, Base)
