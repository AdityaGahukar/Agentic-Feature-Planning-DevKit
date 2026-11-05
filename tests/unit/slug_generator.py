"""
Deterministic Feature Slug Generator and Collision Resolver.
Aligned with Specification v0.2.0 (AD-4) and LLD v1.0.0 (Section 11.3).
"""

import os
import re

STOP_WORDS = {
    "a", "an", "the", "and", "or", "in", "on", "at", "to", "for",
    "with", "by", "from", "of", "is", "it", "as", "be", "this", "that"
}

def generate_feature_slug(feature_statement: str, plans_dir: str = None) -> str:
    """
    Derives a clean, URL-safe, human-readable slug from a feature statement,
    and resolves collisions if a plans directory is provided.

    Rules:
    1. Extract first 6-8 meaningful words (omitting common stop words).
    2. Lowercase and replace non-alphanumeric chars with hyphens.
    3. Collapse consecutive hyphens and truncate to 60 characters maximum.
    4. Suffix with -2, -3, etc. if plans_dir contains a directory with that name.
    """
    if not feature_statement or not feature_statement.strip():
        return "unnamed-feature"

    # Tokenize words
    words = re.findall(r'[a-zA-Z0-9]+', feature_statement.strip())
    
    # Filter stop words while retaining meaningful terms
    filtered_words = [w.lower() for w in words if w.lower() not in STOP_WORDS]
    
    # If all words were stop words, fall back to original words
    if not filtered_words:
        filtered_words = [w.lower() for w in words]
        
    # Take first 6 to 8 words
    selected_words = filtered_words[:8]
    
    # Join with hyphen
    raw_slug = "-".join(selected_words)
    
    # Sanitize: lowercase, non-alphanumeric to hyphens, collapse consecutive hyphens
    sanitized = re.sub(r'[^a-z0-9]+', '-', raw_slug.lower()).strip('-')
    
    # Truncate to 60 chars (without trailing hyphen)
    if len(sanitized) > 60:
        sanitized = sanitized[:60].rstrip('-')
        
    if not sanitized:
        sanitized = "unnamed-feature"

    # If no plans_dir provided, return the sanitized base slug
    if not plans_dir or not os.path.exists(plans_dir):
        return sanitized

    # Collision detection
    candidate_slug = sanitized
    counter = 2
    while os.path.exists(os.path.join(plans_dir, candidate_slug)):
        candidate_slug = f"{sanitized}-{counter}"
        counter += 1

    return candidate_slug
