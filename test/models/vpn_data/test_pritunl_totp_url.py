"""Tests for parsing Pritunl TOTP provisioning URIs."""

import base64
import hashlib

import pytest

from src.models.vpn_model.pritunl_vpn_model import parse_totp_url

# RFC 6238 appendix B SHA1 test key (160 bits), Base32-encoded at runtime.
RFC_6238_SECRET: str = base64.b32encode(b"12345678901234567890").decode()


class TestParseTotpUrl:
    """Verify TOTP URI parsing for server-issued secrets."""

    def test_parse_totp_url_when_rfc_secret_matches_rfc_6238_vector(self) -> None:
        """Generate the RFC 6238 SHA1 8-digit code at T=59."""
        # Arrange
        url = f"otpauth://totp/Pritunl:user?secret={RFC_6238_SECRET}&digits=8"

        # Act
        actual = parse_totp_url(url)

        # Assert
        assert actual.at(59) == "94287082"
        assert actual.issuer == "Pritunl"
        assert actual.name == "user"
        assert actual.digest is hashlib.sha1

    def test_parse_totp_url_when_pritunl_default_80_bit_secret_generates_code(self) -> None:
        """Accept the 16-character Base32 secrets Pritunl issues by default."""
        # Arrange
        url = "otpauth://totp/user@org?secret=JBSWY3DPEHPK3PXP&issuer=pritunl&period=30"

        # Act
        actual = parse_totp_url(url).now()

        # Assert
        assert len(actual) == 6
        assert actual.isdigit()

    @pytest.mark.parametrize(
        "url",
        [
            "https://totp/user?secret=JBSWY3DPEHPK3PXP",
            "otpauth://hotp/user?secret=JBSWY3DPEHPK3PXP",
            "otpauth://totp/user?issuer=pritunl",
            "otpauth://totp/user?secret=JBSWY3DPEHPK3PXP&algorithm=MD5",
            "otpauth://totp/user?secret=TEST_SECRET",
            "otpauth://totp/user?secret=JBSWY3DP",
        ],
    )
    def test_parse_totp_url_when_uri_invalid_raises(self, url: str) -> None:
        """Reject malformed URIs, non-Base32 secrets, and secrets under 80 bits."""
        # Act / Assert
        with pytest.raises(ValueError):
            parse_totp_url(url)
