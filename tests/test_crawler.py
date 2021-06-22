from pytest import mark

from crawler import crawle_dynamic_pages, crawle_static_pages, crawle_phone_numbers


@mark.asyncio
async def test_phones_crawler_static_page():
    url = 'https://repetitors.info'
    data = await crawle_static_pages([url])
    assert data
    assert "84955405676" in data[url]  # from sidebar
    merged_data = await crawle_phone_numbers([url])
    assert sorted(data[url]) == sorted(merged_data[url])


@mark.asyncio
async def test_phones_crawler_dynamic_page():
    url = 'https://hands.ru'
    data = await crawle_dynamic_pages([url])
    assert data
    assert "84951340696" in data[url]  # from footer
    merged_data = await crawle_phone_numbers([url])
    assert sorted(data[url]) == sorted(merged_data[url])
