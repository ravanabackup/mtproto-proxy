import pytest
from pathlib import Path
from unittest.mock import patch, AsyncMock
from src import providers


@pytest.mark.asyncio(loop_scope="function")
@patch("src.providers.asyncio.to_thread")
async def test_aggregate_proxies_success(mock_to_thread, tmp_path: Path):
    test_providers_file = tmp_path / "providers.txt"
    test_raw_proxy_file = tmp_path / "raw_proxy.txt"

    providers.PROVIDERS_PATH = test_providers_file
    providers.RAW_PROXY_PATH = test_raw_proxy_file

    providers_content = (
        "# Test comments, it will be skipped\n"
        "   \n"
        "https://provider-one.com\n"
        "https://provider-two.com\n"
    )

    test_providers_file.write_text(providers_content, encoding="utf-8")
    
    mock_to_thread.side_effect = [
        "https://t.me/proxy?server=1.1.1.1&port=8888&secret=dd213532252354235\n"
        "tg://proxy?server=2.2.2.2&port=8888&secret=dd213532252354235\n",
        
        "tg://proxy?server=1.1.1.1&port=8888&secret=dd213532252354235\n"
        "tg://proxy?server=3.3.3.3&port=8888&secret=dd213532252354235"
    ]

    await providers.aggregate_proxies()

    assert mock_to_thread.call_count == 2
    assert test_raw_proxy_file.exists() is True

    saved_proxies = test_raw_proxy_file.read_text(encoding="utf-8").splitlines()
    
    assert len(saved_proxies) == 4


@pytest.mark.asyncio(loop_scope="function")
@patch("src.providers.asyncio.to_thread")
async def test_aggregate_proxies_no_providers(mock_to_thread, tmp_path: Path):
    test_providers_file = tmp_path / "providers.txt"
    test_raw_proxy_file = tmp_path / "raw_proxy.txt"
    
    providers.PROVIDERS_PATH = test_providers_file
    providers.RAW_PROXY_PATH = test_raw_proxy_file

    test_providers_file.write_text("# no active links", encoding="utf-8")

    await providers.aggregate_proxies()

    mock_to_thread.assert_not_called()
    assert test_raw_proxy_file.exists() is False