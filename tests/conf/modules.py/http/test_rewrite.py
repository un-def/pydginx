from pydginx.conf.modules.http.rewrite import Return


class TestReturn:

    def test_code_only(self):
        ret = Return(403)

        assert ret.code == 403
        assert ret.text is None
        assert ret.url is None
        assert ret.render() == 'return 403;\n'

    def test_code_with_text(self):
        ret = Return(201, 'OK!')

        assert ret.code == 201
        assert ret.text == 'OK!'
        assert ret.url is None
        assert ret.render() == 'return 201 OK!;\n'

    def test_code_with_url(self):
        ret = Return(302, '/redir')

        assert ret.code == 302
        assert ret.text is None
        assert ret.url == '/redir'
        assert ret.render() == 'return 302 /redir;\n'

    def test_url_only(self):
        ret = Return('https://example/com')

        assert ret.code is None
        assert ret.text is None
        assert ret.url == 'https://example/com'
        assert ret.render() == 'return https://example/com;\n'
