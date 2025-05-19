import io
from PIL import Image
import streamlit as st


class ImageProcessor:
    """
    A class to handle image processing, including conversion to base64.

    Args:
        uploaded_file (file-like object): The uploaded image file to be processed.
    """

    def __init__(self, uploaded_file):
        self.uploaded_file = uploaded_file

    def image_to_base64(self, image: Image.Image) -> tuple[bytes, str]:
        """
        Converts an image to base64 encoded string.

        Args:
            image (Image.Image): The image to be converted.

        Returns:
            tuple: A tuple containing the base64 encoded bytes and the MIME type ('image/jpeg').
        """
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        return buffer.getvalue(), "image/jpeg"

    def process_file(
        self, byte_data_key: str = "file_bytes", MIME_type_key: str = "mime_type"
    ) -> None:
        """
        Processes the uploaded file (image or PDF) and stores the resulting byte data and MIME type
        in the Streamlit session state.

        Args:
            byte_data_key (str): The session state key to store the file's byte data. Defaults to "file_bytes".
            MIME_type_key (str): The session state key to store the file's MIME type. Defaults to "mime_type".

        Returns:
            None
        """
        if self.uploaded_file.type == "application/pdf":
            st.session_state[byte_data_key] = self.uploaded_file.read()
            st.session_state[MIME_type_key] = "application/pdf"
        else:
            image = Image.open(self.uploaded_file).convert("RGB")
            st.session_state[byte_data_key], st.session_state[MIME_type_key] = (
                self.image_to_base64(image)
            )
