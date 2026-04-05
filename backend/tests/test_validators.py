import pytest
from backend.validators.input_validator import (
    validate_file,
    validate_extension,
    validate_size,
)
from backend.core.config import get_settings


class TestValidators:
    def test_validate_extension_allowed(self):
        assert validate_extension("document.pdf") == True
        assert validate_extension("document.docx") == True
        assert validate_extension("document.txt") == True

    def test_validate_extension_not_allowed(self):
        assert validate_extension("document.exe") == False
        assert validate_extension("document.java") == False
        assert validate_extension("document.xyz") == False

    def test_validate_size_under_limit(self):
        content = b"a" * 1000
        assert validate_size(content) == True

    def test_validate_size_over_limit(self):
        settings = get_settings()
        content = b"a" * (settings.MAX_FILE_SIZE + 1)
        assert validate_size(content) == False

    def test_validate_file_empty(self):
        with pytest.raises(ValueError, match="Arquivo vazio"):
            validate_file(b"", "test.pdf")

    def test_validate_file_invalid_extension(self):
        with pytest.raises(ValueError, match="Extensão"):
            validate_file(b"test content", "test.exe")
