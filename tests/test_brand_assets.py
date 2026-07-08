from pathlib import Path
import struct


BRAND_DIR = Path("custom_components/chatgpt_usage/brand")


def _png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data.startswith(b"\x89PNG\r\n\x1a\n")
    return struct.unpack(">II", data[16:24])


def test_brand_assets_exist_with_expected_dimensions():
    assert _png_size(BRAND_DIR / "icon.png") == (512, 512)
    assert _png_size(BRAND_DIR / "logo.png") == (1024, 256)
