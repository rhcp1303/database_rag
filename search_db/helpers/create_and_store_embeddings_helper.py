import logging
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


def generate_and_store_embedding(obj, text_field, embedding_field):
    """
    Generates sentence embeddings for a given object's text field and stores them in the object's embedding field.

    This function utilizes the Sentence Transformers library to encode the text from a specified field
    of an object into a dense vector representation (embedding). The generated embedding is then stored
    back into the object in another specified field, and the object is saved.

    Args:
        obj: The object containing the text to be encoded and where the embedding will be stored.
             This object must have attributes corresponding to `text_field` and `embedding_field`,
             and should have a `save()` method.
        text_field (str): The name of the attribute in `obj` that contains the text to be embedded.
        embedding_field (str): The name of the attribute in `obj` where the generated embedding will be stored.

    Returns:
        None. The function modifies the input object in place and saves it.

    Raises:
        AttributeError: If `obj` does not have the specified `text_field` attribute.
        Exception: Any exceptions raised by the Sentence Transformer model or the object's `save()` method.

    Example:
        ```python
        from dataclasses import dataclass

        @dataclass
        class MyObject:
            text: str = ""
            embedding: list = None

            def save(self):
                print(f"Saving object with text: '{self.text}' and embedding: '{self.embedding}'")

        my_obj = MyObject(text="This is a sample sentence.")
        generate_and_store_embedding(my_obj, "text", "embedding")
        ```

    Notes:
        - The function uses the 'all-mpnet-base-v2' Sentence Transformer model. This model is downloaded automatically if it's not already present.
        - The `obj.save()` method is assumed to persist the object's changes to a database or other storage.
        - Error handling is limited to catching exceptions from the Sentence Transformer model and the save operation.
        - If the text field is empty or None, no embedding is generated or saved.
    """
    try:
        model = SentenceTransformer('all-mpnet-base-v2')
        text = getattr(obj, text_field)
        if text:
            embedding = model.encode([text])[0].tolist()
            setattr(obj, embedding_field, embedding)
            obj.save()
        else:
            logger.warning(f"Text field '{text_field}' is empty for object: {obj}")

    except AttributeError as e:
        logger.error(f"AttributeError: {e}")
        raise
    except Exception as e:
        logger.error(f"An error occurred during embedding generation or saving: {e}")
        raise