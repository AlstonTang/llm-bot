from ddgs import ddgs
from functools import wraps

ddgsInstance = ddgs.DDGS()

def debug(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print(f"--- Calling {f.__name__} ---")
        print(f"Args: {args}, Kwargs: {kwargs}")
        
        result = f(*args, **kwargs)
        
        print(f"Result: {result}")
        print("-" * (14 + len(f.__name__)))
        return result
    return wrap

@debug
def search(query: str, *args, **kwargs) -> str:
    """Get online search results. Useful for finding real-time or factual information.
    
    :param query: The query to pass into the search engine
    :type query: str
    :returns: Search results.
    :rtype: str
    """ 

    if args:
        print(f"Warning: Ignoring extra positional arguments: {args}")
    if kwargs:
        print(f"Warning: Ignoring extra keyword arguments: {kwargs}")

    try:
        response = ddgsInstance.text(query)
        
        if response:
            return(f"{str(response)}")
        else:
            return("No answer found for this topic.")
            
    except Exception as e:
        print(f"An error occurred: {e}")