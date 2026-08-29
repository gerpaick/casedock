from django.test import Client
from django.urls import reverse


def test_homepage_renders(client, db):
    response = client.get(reverse("ui:home"))

    assert response.status_code == 200
    assert b"Keep the right work in front." in response.content
    assert b"data-board-home" in response.content


class TestTrustPages:
    """Public Help / Privacy / Terms — basic placeholder content.

    Routes are anonymous-accessible (legal pages) and must resolve to 200.
    Full Stage 10.1-10.3 acceptance (5 FAQ, EU-legal review) is
    tracked in tasks.md — these tests guard the partial version from ADR
    2026-07-30.
    """

    @staticmethod
    def _anon() -> Client:
        return Client()

    def test_help_page_renders_for_anonymous(self, db):
        response = self._anon().get(reverse("help"))
        assert response.status_code == 200
        assert b"How casedock works." in response.content
        assert b"help@casedock.local" in response.content

    def test_privacy_page_renders_for_anonymous(self, db):
        response = self._anon().get(reverse("privacy"))
        assert response.status_code == 200
        assert b"What casedock stores" in response.content
        assert b"privacy@casedock.local" in response.content

    def test_terms_page_renders_for_anonymous(self, db):
        response = self._anon().get(reverse("terms"))
        assert response.status_code == 200
        assert b"agreement between you and casedock" in response.content
        assert b"As is" in response.content

    def test_trust_pages_reachable_when_authenticated(self, client):
        for name in ("help", "privacy", "terms"):
            response = client.get(reverse(name))
            assert response.status_code == 200, name

    def test_footer_renders_resolved_trust_links(self, client):
        response = client.get(reverse("ui:home"))
        assert response.status_code == 200
        assert reverse("help").encode() in response.content
        assert reverse("privacy").encode() in response.content
        assert reverse("terms").encode() in response.content
