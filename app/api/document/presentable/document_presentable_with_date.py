from app.api.document.presentable.document_presentable import (
    DocumentPresentable,
)
from app.domain.entities.with_date_entity import WithDateModel


class DocumentPresentableWithDate(DocumentPresentable, WithDateModel):
    pass
