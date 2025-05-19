import google.generativeai as genai


def query_gemini(prompt: str, file_bytes: bytes, mime_type: str) -> str:
    """
    Queries the Gemini API with a given prompt and file data to generate content.

    Args:
        prompt (str): The prompt to send to the model for processing.
        file_bytes (bytes): The file data to be processed by the model (e.g., image or PDF bytes).
        mime_type (str): The MIME type of the file (e.g., 'image/jpeg', 'application/pdf').

    Returns:
        str: The generated response content from the Gemini model.
    """
    model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")
    response = model.generate_content(
        [prompt, {"mime_type": mime_type, "data": file_bytes}]
    )
    return response.text
