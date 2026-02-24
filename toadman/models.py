from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Article:
    title: str
    url: str
    published_date: Optional[datetime]
    source: str
    content_snippet: str
    category: str = "general"
