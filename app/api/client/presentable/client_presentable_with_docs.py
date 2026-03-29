from app.api.client.presentable.client_presentable import ClientPresentable
from app.api.document.presentable.document_presentable import (
    DocumentPresentable,
)


class ClientPresentableWithDocuments(ClientPresentable):
    documents: list[DocumentPresentable]
