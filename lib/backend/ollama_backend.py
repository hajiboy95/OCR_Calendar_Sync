import ollama
import base64


def query_ollama(prompt: str, file_bytes: bytes, mime_type: str, model: str) -> str:
    """
    Queries the Ollama model with a given prompt and file data to generate content.

    Args:
        prompt (str): The prompt to send to the model for processing.
        file_bytes (bytes): The file data to be processed by the model (e.g., image bytes).
        mime_type (str): The MIME type of the file (e.g., 'image/jpeg').
        model (str): The name of the Ollama model to use (e.g., 'llama3', 'llava').

    Returns:
        str: The generated response content from the Ollama model.

    Raises:
        ValueError: If the file type is a PDF, as it cannot be processed by Ollama.
    """
    if mime_type == "application/pdf":
        raise ValueError(
            "PDF-Dateien können nur mit dem Gemini-Modell verarbeitet werden."
        )

    base64_data = base64.b64encode(file_bytes).decode()
    response = ollama.chat(
        model=model,  # Ensure the correct model name
        messages=[{"role": "user", "content": prompt, "images": [base64_data]}],
    )
    return response["message"]["content"]
