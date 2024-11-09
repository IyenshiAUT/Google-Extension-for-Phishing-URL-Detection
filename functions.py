import re
from urllib.parse import urlparse
import math
import tldextract
import ipaddress
from collections import Counter

# 1. URL length
def url_length(url):
    return len(url)

# 2. Start with IP (Check if base URL is an IP address)
def is_ip_address(url):
    # Parse the URL to extract the hostname
    hostname = urlparse(url).hostname
    try:
        # Check if base_url is a valid IP address
        ipaddress.ip_address(hostname)
        return 1
    except ValueError:
        # If ip_address() raises a ValueError, it's not an IP address
        return 0

# 3. URL entropy
def calculate_entropy(url):
    # Count the frequency of each character in the URL
    counter = Counter(url)
    length = len(url)   
    # Calculate the entropy
    entropy = 0
    for count in counter.values():
        # Calculate the probability of each character
        p_x = count / length
        # Add to entropy, using log base 2
        entropy += -p_x * math.log2(p_x)
    
    return entropy


# 4. Dot count
def dot_count(url):
    return url.count('.')

# 5. At (@) count
def at_count(url):
    return url.count('@')

# 6. Dash (-) count
def dash_count(url):
    return url.count('-')

# 7. Has punycode
def has_punycode(url):
    parsed_url = urlparse(url)
    domain = parsed_url.hostname
    
    try:
        availability = domain.startswith("xn--")
        if availability == True:
            return 1
        else:
            return 0
    except:
        return 0

# 8. Digit-letter ratio
def digit_letter_ratio(url):
    digits = len(re.findall(r'\d', url))
    letters = len(re.findall(r'[a-zA-Z]', url))
    if letters == 0:
        return 0
    else:
        return digits / (letters)

# 9. Contains TLD in subdirectory
def contains_tld_in_subdirectory(url):
    tlds = ['.com', '.org', '.net', '.edu', '.gov', '.co', '.us', '.uk', '.in', '.io', '.info', '.xyz', '.biz', '.me', '.tv', '.online', '.site']
    
    try:
        parsed_url = urlparse(url)
        subdirectory = parsed_url.path
        
        for tld in tlds:
            if tld in subdirectory:
                return 1
        return 0
    except:
        return 0

# 10. Domain has digits
def domain_has_digits(url):
    try:
        # Parse the URL and extract the hostname (domain)
        hostname = urlparse(url).hostname
        
        # Check if the hostname contains any digits (0-9)
        if re.search(r'\d', hostname):  # Search for digits in the hostname
            return 1
        return 0
    except:
        return 0

# 11. Subdomain count
def subdomain_count(url):
    try:
        parsed_url = urlparse(url)
        domain_parts = parsed_url.hostname.split('.')
        if len(domain_parts)>2:
            return len(domain_parts) - 2  # Subtracting the domain and TLD
        else:
            return 0
    except:
        return 0

# 12. Character entropy of non-alphanumeric characters
def calculate_char_entropy(url):
    # Extract all non-alphanumeric characters from the URL using a regular expression
    non_alnum_chars = re.findall(r'[^a-zA-Z0-9]', url)
    
    # If no non-alphanumeric characters found, return 0 entropy
    if not non_alnum_chars:
        return 0
    
    # Count the frequency of each character
    char_counts = Counter(non_alnum_chars)
    
    # Calculate the total number of non-alphanumeric characters
    total_chars = len(non_alnum_chars)
    
    # Calculate entropy
    entropy = 0
    for count in char_counts.values():
        probability = count / total_chars
        entropy -= probability * math.log2(probability)
    
    return entropy

# 13. Has internal links (Check if target URL belongs to the same domain as base URL)
def has_internal_links(url):
    extracted = tldextract.extract(url)
    try:
        if url ==extracted:
            return 1
        else:
            return 0
    except:
        return 0

