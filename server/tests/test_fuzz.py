import uuid

import pytest

from tests.conftest import ADMIN_KEY, bearer, login, register, unique



class TestRegisterFuzz:
    def test_empty_username(self, client):
        r = register(client, "")
        assert r.status_code in (409,)

    def test_empty_password(self, client):
        r = client.post("/api/v1/auth/register", json={"username": unique(), "password": "", "role": "collector"})
        assert r.status_code not in (500,)

    def test_very_long_username(self, client):
        r = register(client, "a" * 10_000)
        assert r.status_code not in (500,)

    def test_very_long_password(self, client):
        r = register(client, unique(), password="x" * 10_000)
        assert r.status_code not in (500,)

    def test_sql_injection_username(self, client):
        r = register(client, "'; DROP TABLE users; --")
        assert r.status_code not in (500,)

    def test_xss_in_username(self, client):
        r = register(client, "<script>alert(1)</script>")
        assert r.status_code not in (500,)

    def test_unicode_username(self, client):
        r = register(client, "用户名_😀_тест")
        assert r.status_code not in (500,)

    def test_null_byte_in_username(self, client):
        r = register(client, "user\x00name")
        assert r.status_code not in (500,)

    def test_invalid_role(self, client):
        r = client.post("/api/v1/auth/register", json={"username": unique(), "password": "pass", "role": "superuser"})
        assert r.status_code == 422

    def test_admin_role_without_key(self, client):
        r = client.post("/api/v1/auth/register", json={"username": unique(), "password": "pass", "role": "admin"})
        assert r.status_code == 403

    def test_admin_role_wrong_key(self, client):
        r = client.post(
            "/api/v1/auth/register",
            json={"username": unique(), "password": "pass", "role": "admin", "admin_key": "wrong-key"},
        )
        assert r.status_code == 403

    def test_duplicate_username(self, client):
        name = unique()
        register(client, name)
        r = register(client, name)
        assert r.status_code == 409

    def test_missing_username_field(self, client):
        r = client.post("/api/v1/auth/register", json={"password": "pass"})
        assert r.status_code == 422

    def test_missing_password_field(self, client):
        r = client.post("/api/v1/auth/register", json={"username": unique()})
        assert r.status_code == 422

    def test_wrong_content_type(self, client):
        r = client.post(
            "/api/v1/auth/register",
            content="username=foo&password=bar",
            headers={"Content-Type": "text/plain"},
        )
        assert r.status_code in (415, 422)

    def test_numeric_username_coerced_or_rejected(self, client):
        r = client.post("/api/v1/auth/register", json={"username": 12345, "password": "pass"})
        assert r.status_code not in (500,)

    def test_null_username(self, client):
        r = client.post("/api/v1/auth/register", json={"username": None, "password": "pass"})
        assert r.status_code == 422

    def test_empty_body(self, client):
        r = client.post("/api/v1/auth/register", json={})
        assert r.status_code == 422


class TestLoginFuzz:
    def test_nonexistent_user(self, client):
        r = login(client, "ghost_user_does_not_exist", "wrong")
        assert r.status_code == 401

    def test_wrong_password(self, client):
        name = unique()
        register(client, name, password="correct_password")
        r = login(client, name, password="wrong_password")
        assert r.status_code == 401

    def test_empty_username(self, client):
        r = login(client, "", "pass")
        assert r.status_code in (400, 401, 422)

    def test_empty_password(self, client):
        r = login(client, "someone", "")
        assert r.status_code in (400, 401, 422)

    def test_sql_injection_in_credentials(self, client):
        r = login(client, "' OR '1'='1", "' OR '1'='1")
        assert r.status_code not in (500,)

    def test_very_long_username(self, client):
        r = login(client, "a" * 10_000, "pass")
        assert r.status_code not in (500,)

    def test_get_method_not_allowed(self, client):
        r = client.get("/api/v1/auth/token")
        assert r.status_code == 405

    def test_json_body_rejected_expects_form(self, client):
        r = client.post("/api/v1/auth/token", json={"username": "foo", "password": "bar"})
        assert r.status_code == 422


class TestAuthBypassFuzz:
    PROTECTED = "/api/v1/users/me"

    def test_no_auth_header(self, client):
        r = client.get(self.PROTECTED)
        assert r.status_code == 401

    def test_wrong_scheme_basic(self, client):
        r = client.get(self.PROTECTED, headers={"Authorization": "Basic dXNlcjpwYXNz"})
        assert r.status_code == 401

    @pytest.mark.parametrize("token", [
        "not-a-jwt",
        "eyJhbGciOiJIUzI1NiJ9.e30.invalidsig",
        "null",
        "undefined",
        " ",
        "a" * 500,
        "Bearer",
        "",
    ])
    def test_invalid_token(self, client, token):
        r = client.get(self.PROTECTED, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 401


class TestCreateMasterCardFuzz:
    VALID = {"title": "T", "symbol": "S", "rarity": "common", "description": "D", "quantity": 1}
    URL = "/api/v1/master-cards/"

    def test_no_auth(self, client):
        r = client.post(self.URL, json=self.VALID)
        assert r.status_code == 401

    def test_collector_forbidden(self, client, collector_token):
        r = client.post(self.URL, json=self.VALID, headers=bearer(collector_token))
        assert r.status_code == 403

    def test_missing_title(self, client, admin_token):
        body = {k: v for k, v in self.VALID.items() if k != "title"}
        r = client.post(self.URL, json=body, headers=bearer(admin_token))
        assert r.status_code == 422

    def test_missing_quantity(self, client, admin_token):
        body = {k: v for k, v in self.VALID.items() if k != "quantity"}
        r = client.post(self.URL, json=body, headers=bearer(admin_token))
        assert r.status_code == 422

    def test_zero_quantity(self, client, admin_token):
        r = client.post(self.URL, json={**self.VALID, "quantity": 0}, headers=bearer(admin_token))
        assert r.status_code == 422

    def test_negative_quantity(self, client, admin_token):
        r = client.post(self.URL, json={**self.VALID, "quantity": -1}, headers=bearer(admin_token))
        assert r.status_code == 422

    def test_invalid_rarity(self, client, admin_token):
        r = client.post(self.URL, json={**self.VALID, "rarity": "mythic"}, headers=bearer(admin_token))
        assert r.status_code == 422

    def test_null_title(self, client, admin_token):
        r = client.post(self.URL, json={**self.VALID, "title": None}, headers=bearer(admin_token))
        assert r.status_code == 422

    def test_very_long_title(self, client, admin_token):
        r = client.post(self.URL, json={**self.VALID, "title": "A" * 50_000}, headers=bearer(admin_token))
        assert r.status_code not in (500,)

    def test_very_long_description(self, client, admin_token):
        r = client.post(self.URL, json={**self.VALID, "description": "D" * 50_000}, headers=bearer(admin_token))
        assert r.status_code not in (500,)

    def test_xss_in_title(self, client, admin_token):
        r = client.post(self.URL, json={**self.VALID, "title": "<img src=x onerror=alert(1)>"}, headers=bearer(admin_token))
        assert r.status_code not in (500,)

    def test_very_large_quantity(self, client, admin_token):
        r = client.post(self.URL, json={**self.VALID, "quantity": 2**31}, headers=bearer(admin_token))
        assert r.status_code not in (500,)

    def test_empty_body(self, client, admin_token):
        r = client.post(self.URL, json={}, headers=bearer(admin_token))
        assert r.status_code == 422

    @pytest.mark.parametrize("rarity", ["common", "uncommon", "rare", "epic", "legendary"])
    def test_all_valid_rarities_accepted(self, client, admin_token, rarity):
        r = client.post(self.URL, json={**self.VALID, "rarity": rarity}, headers=bearer(admin_token))
        assert r.status_code == 201


class TestGetMasterCardFuzz:
    def test_no_auth_list(self, client):
        r = client.get("/api/v1/master-cards/")
        assert r.status_code == 401

    def test_list_returns_array(self, client, collector_token):
        r = client.get("/api/v1/master-cards/", headers=bearer(collector_token))
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_invalid_uuid_in_path(self, client, collector_token):
        r = client.get("/api/v1/master-cards/not-a-uuid", headers=bearer(collector_token))
        assert r.status_code == 422

    def test_random_uuid_not_found(self, client, collector_token):
        r = client.get(f"/api/v1/master-cards/{uuid.uuid4()}", headers=bearer(collector_token))
        assert r.status_code == 404

    def test_path_traversal_attempt(self, client, collector_token):
        r = client.get("/api/v1/master-cards/../auth/token", headers=bearer(collector_token))
        assert r.status_code in (404, 405, 422)

    def test_no_auth_get_by_id(self, client, card_id):
        r = client.get(f"/api/v1/master-cards/{card_id}")
        assert r.status_code == 401


class TestUpdateMasterCardFuzz:
    URL = "/api/v1/master-cards/{id}"

    def test_no_auth(self, client, card_id):
        r = client.patch(self.URL.format(id=card_id), json={"title": "X"})
        assert r.status_code == 401

    def test_collector_forbidden(self, client, card_id, collector_token):
        r = client.patch(self.URL.format(id=card_id), json={"title": "X"}, headers=bearer(collector_token))
        assert r.status_code == 403

    def test_invalid_uuid(self, client, admin_token):
        r = client.patch("/api/v1/master-cards/bad-id", json={"title": "X"}, headers=bearer(admin_token))
        assert r.status_code == 422

    def test_nonexistent_card(self, client, admin_token):
        r = client.patch(self.URL.format(id=uuid.uuid4()), json={"title": "X"}, headers=bearer(admin_token))
        assert r.status_code == 404

    def test_zero_quantity_rejected(self, client, card_id, admin_token):
        r = client.patch(self.URL.format(id=card_id), json={"quantity": 0}, headers=bearer(admin_token))
        assert r.status_code == 422

    def test_negative_quantity_rejected(self, client, card_id, admin_token):
        r = client.patch(self.URL.format(id=card_id), json={"quantity": -5}, headers=bearer(admin_token))
        assert r.status_code == 422

    def test_invalid_rarity_rejected(self, client, card_id, admin_token):
        r = client.patch(self.URL.format(id=card_id), json={"rarity": "legendary-plus"}, headers=bearer(admin_token))
        assert r.status_code == 422

    def test_empty_patch_no_crash(self, client, card_id, admin_token):
        r = client.patch(self.URL.format(id=card_id), json={}, headers=bearer(admin_token))
        assert r.status_code not in (500,)


class TestDeleteMasterCardFuzz:
    URL = "/api/v1/master-cards/{id}"

    def test_no_auth(self, client, card_id):
        r = client.delete(self.URL.format(id=card_id))
        assert r.status_code == 401

    def test_collector_forbidden(self, client, card_id, collector_token):
        r = client.delete(self.URL.format(id=card_id), headers=bearer(collector_token))
        assert r.status_code == 403

    def test_invalid_uuid(self, client, admin_token):
        r = client.delete("/api/v1/master-cards/not-valid", headers=bearer(admin_token))
        assert r.status_code == 422

    def test_nonexistent_card(self, client, admin_token):
        r = client.delete(self.URL.format(id=uuid.uuid4()), headers=bearer(admin_token))
        assert r.status_code == 404


class TestCollectionFuzz:
    def test_admin_cannot_collect(self, client, card_id, admin_token):
        r = client.post("/api/v1/collection/", json={"master_card_id": card_id}, headers=bearer(admin_token))
        assert r.status_code == 403

    def test_no_auth_collect(self, client, card_id):
        r = client.post("/api/v1/collection/", json={"master_card_id": card_id})
        assert r.status_code == 401

    def test_collect_nonexistent_card(self, client, collector_token):
        r = client.post("/api/v1/collection/", json={"master_card_id": str(uuid.uuid4())}, headers=bearer(collector_token))
        assert r.status_code == 404

    def test_collect_invalid_uuid(self, client, collector_token):
        r = client.post("/api/v1/collection/", json={"master_card_id": "not-a-uuid"}, headers=bearer(collector_token))
        assert r.status_code == 422

    def test_collect_missing_field(self, client, collector_token):
        r = client.post("/api/v1/collection/", json={}, headers=bearer(collector_token))
        assert r.status_code == 422

    def test_collect_null_card_id(self, client, collector_token):
        r = client.post("/api/v1/collection/", json={"master_card_id": None}, headers=bearer(collector_token))
        assert r.status_code == 422

    def test_no_auth_list(self, client):
        r = client.get("/api/v1/collection/")
        assert r.status_code == 401

    def test_admin_cannot_list_collection(self, client, admin_token):
        r = client.get("/api/v1/collection/", headers=bearer(admin_token))
        assert r.status_code == 403

    def test_no_auth_delete(self, client):
        r = client.delete(f"/api/v1/collection/{uuid.uuid4()}")
        assert r.status_code == 401

    def test_admin_cannot_delete_from_collection(self, client, admin_token):
        r = client.delete(f"/api/v1/collection/{uuid.uuid4()}", headers=bearer(admin_token))
        assert r.status_code == 403

    def test_delete_invalid_uuid(self, client, collector_token):
        r = client.delete("/api/v1/collection/bad-id", headers=bearer(collector_token))
        assert r.status_code == 422

    def test_delete_nonexistent_collected_card(self, client, collector_token):
        r = client.delete(f"/api/v1/collection/{uuid.uuid4()}", headers=bearer(collector_token))
        assert r.status_code == 404

    def test_out_of_stock_card_returns_409(self, client, admin_token, collector_token):
        r = client.post(
            "/api/v1/master-cards/",
            json={"title": "Limited", "symbol": "LTD", "rarity": "epic", "description": "only one", "quantity": 1},
            headers=bearer(admin_token),
        )
        assert r.status_code == 201
        limited_id = r.json()["id"]

        r1 = client.post("/api/v1/collection/", json={"master_card_id": limited_id}, headers=bearer(collector_token))
        assert r1.status_code == 201

        r2 = client.post("/api/v1/collection/", json={"master_card_id": limited_id}, headers=bearer(collector_token))
        assert r2.status_code == 409
