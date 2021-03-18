import just
import requests_mock
import pytest

NOT_EXISTING_URL = "mock://stuasdfasfasdfasf.com"


@pytest.mark.parametrize(
    "method, output, content_type",
    [
        ("GET", "mock_text", "text/html"),
        ("GET", {"mock": "text"}, "application/json"),
        ("POST", "mock_text", "text/html"),
        ("POST", {"mock": "text"}, "application/json"),
    ],
)
def test_requests(method, output, content_type):
    with requests_mock.mock() as m:
        headers = {"Content-Type": content_type}
        just_method = just.get if method == "GET" else just.post
        m_method = m.get if method == "GET" else m.post
        if content_type == "application/json":
            m_method(NOT_EXISTING_URL, json=output, headers=headers)
            assert just_method(NOT_EXISTING_URL) == output
        else:
            m_method(NOT_EXISTING_URL, text=output, headers=headers)
            assert just_method(NOT_EXISTING_URL) == output


def test_retry():
    assert not just.get(NOT_EXISTING_URL, max_retries=2, delay_base=0.01)
