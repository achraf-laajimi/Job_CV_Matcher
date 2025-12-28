# app/utils/ollama_async.py
"""
Async wrapper for Ollama synchronous client.
Only for LLM chat operations - embeddings now use transformers.
"""

import asyncio
import ollama
from functools import partial
from typing import List, Dict, Any, Optional


async def chat_async(
    model: str,
    messages: List[Dict[str, str]],
    format: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Async wrapper for ollama.chat.
    
    Args:
        model: Model name (e.g., "llama3.1:8b")
        messages: List of message dictionaries
        format: Output format (e.g., "json")
        options: Model options (e.g., {"num_predict": 500})
        
    Returns:
        Response dictionary from Ollama
    """
    loop = asyncio.get_event_loop()
    
    # Optimize memory and speed with default options
    if options is None:
        options = {}
    
    options.setdefault("num_ctx", 2048)      # Context window (smaller = faster + less RAM)
    options.setdefault("num_predict", 500)   # Max output tokens
    
    func = partial(
        ollama.chat,
        model=model,
        messages=messages,
        format=format,
        options=options
    )
    return await loop.run_in_executor(None, func)
