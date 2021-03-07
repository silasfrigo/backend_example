from diskcache import Cache


_file_cache = None


def get_file_cache():
    global _file_cache

    if _file_cache is None:
        _file_cache = Cache('/tmp/project_cache')

    return _file_cache


file_cache = get_file_cache()
