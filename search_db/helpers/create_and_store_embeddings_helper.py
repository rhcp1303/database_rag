import logging
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


def generate_and_store_embedding(obj, text_field, embedding_field):
    model = SentenceTransformer('all-mpnet-base-v2')
    text = getattr(obj, text_field)
    if text:
        embedding = model.encode([text])[0].tolist()
        setattr(obj, embedding_field, embedding)
        obj.save()
