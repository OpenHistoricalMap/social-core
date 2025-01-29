import json

from httpretty import HTTPretty

from .oauth import BaseAuthUrlTestMixin, OAuth2Test


class AmazonOAuth2Test(OAuth2Test, BaseAuthUrlTestMixin):
    backend_path = "social_core.backends.amazon.AmazonOAuth2"
    user_data_url = "https://api.amazon.com/user/profile"
    expected_username = "FooBar"
    access_token_body = json.dumps({"access_token": "foobar", "token_type": "bearer"})
    user_data_body = json.dumps(
        {
            "user_id": "amzn1.account.ABCDE1234",
            "email": "foo@bar.com",
            "name": "Foo Bar",
        }
    )

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()


class AmazonOAuth2BrokenServerResponseTest(OAuth2Test, BaseAuthUrlTestMixin):
    backend_path = "social_core.backends.amazon.AmazonOAuth2"
    user_data_url = "https://www.amazon.com/ap/user/profile"
    expected_username = "FooBar"
    access_token_body = json.dumps({"access_token": "foobar", "token_type": "bearer"})
    user_data_body = json.dumps(
        {
            "Request-Id": "02GGTU7CWMNFTV3KH3J6",
            "Profile": {
                "Name": "Foo Bar",
                "CustomerId": "amzn1.account.ABCDE1234",
                "PrimaryEmail": "foo@bar.com",
            },
        }
    )

    def setUp(self):
        super().setUp()
        HTTPretty.register_uri(
            HTTPretty.GET,
            "https://api.amazon.com/user/profile",
            status=200,
            body=self.user_data_body,
            content_type="application/json",
        )

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()
