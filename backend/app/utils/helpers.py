import re
import uuid
import logging
from typing import List
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def generate_job_id() -> str:
    """Generate a unique job ID."""
    return str(uuid.uuid4())


def extract_domain(url: str) -> str:
    """
    Extract domain from URL.
    
    Args:
        url: Full URL
        
    Returns:
        Domain name
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "")
        return domain
    except Exception as e:
        logger.error(f"Error extracting domain from {url}: {str(e)}")
        return url


def validate_urls(urls: List[str]) -> tuple[bool, List[str]]:
    """
    Validate a list of URLs.
    
    Args:
        urls: List of URLs to validate
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    if not urls:
        errors.append("No URLs provided")
        return False, errors
    
    if len(urls) > 5:
        errors.append("Maximum 5 URLs allowed per analysis")
        return False, errors
    
    for url in urls:
        if not url.startswith(("http://", "https://")):
            errors.append(f"Invalid URL format: {url}")
        
        try:
            result = urlparse(url)
            if not result.netloc:
                errors.append(f"Invalid URL: {url}")
        except Exception as e:
            errors.append(f"Error parsing URL {url}: {str(e)}")
    
    return len(errors) == 0, errors


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Raw text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    text = normalize_text(text)
    return text


def normalize_text(text: str) -> str:
    """
    Normalize whitespace, punctuation, and simple markup in text.
    """
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([.,!?;:])", r"\1", text)
    return text.strip()


def clean_html(html: str) -> str:
    """
    Clean HTML content by removing scripts, styles, and comments.
    """
    if not html:
        return ""
    html = re.sub(r"<script[\s\S]*?</script>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"<style[\s\S]*?</style>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
    return html.strip()


def calculate_reading_time(text: str) -> int:
    """
    Calculate estimated reading time in minutes.
    
    Args:
        text: Full text
        
    Returns:
        Estimated reading time in minutes
    """
    if not text:
        return 0
    
    word_count = len(text.split())
    reading_speed = 200  # Average words per minute
    
    return max(1, round(word_count / reading_speed))


def get_suggestion_priority(score: float) -> str:
    """
    Get priority level based on score.
    
    Args:
        score: Score 0-10
        
    Returns:
        Priority level
    """
    if score < 4.0:
        return "High"
    elif score < 6.5:
        return "Medium"
    else:
        return "Low"


def format_percentage(value: float, total: float) -> str:
    """
    Format a value as percentage.
    
    Args:
        value: Numerator
        total: Denominator
        
    Returns:
        Formatted percentage string
    """
    if total == 0:
        return "0%"
    
    percentage = (value / total) * 100
    return f"{percentage:.1f}%"
