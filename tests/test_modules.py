import importlib

MODULES = [
    "webshell_dir",
    "webshell_name",
    "reverse_ip",
    "subdomain",
    "env_debug",
    "extract_domain",
    "wp_register",
    "domain_by_date",
    "haxor_grab",
    "zoneh_grab",
    "ftp_brute",
    "ftp_client",
    "proxy_validator",
]


def test_modules_importable():
    for name in MODULES:
        mod = importlib.import_module(f"modules.{name}")
        assert hasattr(mod, "run")


def test_normalize():
    from modules.extract_domain import normalize

    assert normalize("example.com") == "https://example.com"
    assert normalize("https://example.com/path?q=1") == "https://example.com"
    assert normalize("http://example.com") == "http://example.com"
    assert normalize("   ") is None
