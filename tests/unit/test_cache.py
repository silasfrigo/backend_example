from cache import file_cache


def test_file_cache():
    assert not file_cache.get('sample')
    file_cache.set(key='sample', value='exists')
    assert file_cache.get('sample') == 'exists'
