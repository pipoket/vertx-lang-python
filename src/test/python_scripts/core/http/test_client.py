# Copyright 2011-2012 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import vertx
from test_utils import TestUtils
from core.buffer import Buffer

tu = TestUtils()
tu.check_thread()
server = vertx.create_http_server()
client = vertx.create_http_client()
client.port = 8080
logger = vertx.logger()

# This is just a basic test. Most testing occurs in the Java tests
class HttpTest(object):
    def test_get(self):
        http_method(False, "GET", False)

    def test_get_ssl(self):
        http_method(True, "GET", False)

    def test_put(self):
        http_method(False, "PUT", False)

    def test_put_ssl(self):
        http_method(True, "PUT", False)

    def test_post(self):
        http_method(False, "POST", False)

    def test_post_ssl(self):
        http_method(True, "POST", False)

    def test_head(self):
        http_method(False, "HEAD", False)

    def test_head_ssl(self):
        http_method(True, "HEAD", False)

    def test_options(self):
        http_method(False, "OPTIONS", False)

    def test_options_ssl(self):
        http_method(True, "OPTIONS", False)

    def test_delete(self):
        http_method(False, "DELETE", False)

    def test_delete_ssl(self):
        http_method(True, "DELETE", False)

    def test_trace(self):
        http_method(False, "TRACE", False)

    def test_trace_ssl(self):
        http_method(True, "TRACE", False)

    def test_connect(self):
        http_method(False, "CONNECT", False)

    def test_connect_ssl(self):
        http_method(True, "CONNECT", False)

    def test_patch(self):
        http_method(False, "PATCH", False)

    def test_patch_ssl(self):
        http_method(True, "PATCH", False)

    def test_get_chunked(self):
        http_method(False, "GET", True)

    def test_get_ssl_chunked(self):
        http_method(True, "GET", True)

    def test_put_chunked(self):
        http_method(False, "PUT", True)

    def test_put_ssl_chunked(self):
        http_method(True, "PUT", True)

    def test_post_chunked(self):
        http_method(False, "POST", True)

    def test_post_ssl_chunked(self):
        http_method(True, "POST", True)

    def test_head_chunked(self):
        http_method(False, "HEAD", True)

    def test_head_ssl_chunked(self):
        http_method(True, "HEAD", True)

    def test_options_chunked(self):
        http_method(False, "OPTIONS", True)

    def test_options_ssl_chunked(self):
        http_method(True, "OPTIONS", True)

    def test_delete_chunked(self):
        http_method(False, "DELETE", True)

    def test_delete_ssl_chunked(self):
        http_method(True, "DELETE", True)

    def test_trace_chunked(self):
        http_method(False, "TRACE", True)

    def test_trace_ssl_chunked(self):
        http_method(True, "TRACE", True)

    def test_connect_chunked(self):
        http_method(False, "CONNECT", True)

    def test_connect_ssl_chunked(self):
        http_method(True, "CONNECT", True)

    def test_patch_chunked(self):
        http_method(False, "PATCH", True)

    def test_patch_ssl_chunked(self):
        http_method(True, "PATCH", True)

    def test_form_file_upload(self):
        content = "Vert.x rocks!"
        @server.request_handler
        def request_handler(req):
            if req.uri == '/form':
                req.response.chunked = True
                req.expect_multipart = True
                @req.upload_handler
                def upload_handler(upload):
                    tu.azzert('tmp-0.txt' == upload.filename)
                    tu.azzert('image/gif' == upload.content_type)
                    @upload.data_handler
                    def data_handler(buffer):
                        tu.azzert(content == buffer.to_string())

                @req.end_handler
                def end_handler():
                    attrs = req.form_attributes
                    tu.azzert(attrs.is_empty)
                    req.response.end()

        def listen_handler (err, serv):
            tu.azzert(err is None)
            client.port = 8080

            def post_handler(resp):
                # assert the response
                tu.azzert(200 == resp.status_code)
                @resp.body_handler
                def body_handler(body):
                    tu.azzert(0 == body.length)
                tu.test_complete()

            req = client.post("/form", post_handler)
            boundary = "dLV9Wyq26L_-JQxk6ferf-RT153LhOO"
            buffer = Buffer.create()
            b = "--" + boundary + "\r\n" + "Content-Disposition: form-data; name=\"file\"; filename=\"tmp-0.txt\"\r\n" + "Content-Type: image/gif\r\n" + "\r\n" + content + "\r\n" + "--" + boundary + "--\r\n"

            buffer.append_str(b)
            req.put_header('content-length', str(buffer.length))
            req.put_header('content-type', 'multipart/form-data; boundary=' + boundary)
            req.write(buffer).end()

        server.listen(8080, "0.0.0.0", listen_handler)

    def test_form_upload_attributes(self):
        @server.request_handler
        def request_handler(req):
            if req.uri == '/form':
                req.response.chunked = True
                req.expect_multipart = True
                @req.upload_handler
                def upload_handler(event):
                    @event.data_handler
                    def data_handler(buffer):
                        tu.azzert(False)

                @req.end_handler
                def end_handler():
                    attrs = req.form_attributes
                    tu.azzert(attrs['framework'] == 'vertx')
                    tu.azzert(attrs['runson'] == 'jvm')
                    req.response.end()

        def listen_handler (err, serv):
            tu.azzert(err is None)
            client.port = 8080

            def post_handler(resp):
                # assert the response
                tu.azzert(200 == resp.status_code)
                @resp.body_handler
                def body_handler(body):
                    tu.azzert(0 == body.length)
                tu.test_complete()

            req = client.post("/form", post_handler)
            buffer = Buffer.create()
            buffer.append_str('framework=vertx&runson=jvm')
            req.put_header('content-length', str(buffer.length))
            req.put_header('content-type', 'application/x-www-form-urlencoded')
            req.write(buffer).end()

        server.listen(8080, "0.0.0.0", listen_handler)



def http_method(ssl, method, chunked):

    logger.info("in http method %s"% method)

    server.compression_supported = True
    tu.azzert(server.compression_supported)

    if ssl:
        server.ssl = True
        server.key_store_path = './src/test/keystores/server-keystore.jks'
        server.key_store_password = 'wibble'
        server.trust_store_path = './src/test/keystores/server-truststore.jks'
        server.trust_store_password = 'wibble'
        server.client_auth_required = True

    path = "/someurl/blah.html"
    query = "param1=vparam1&param2=vparam2"
    uri = "http://localhost:8080" + path + "?" + query;

    @server.request_handler
    def request_handler(req):
        tu.check_thread()
        tu.azzert(req.version == 'HTTP_1_1')
        tu.azzert(req.uri == uri)
        tu.azzert(req.method == method)
        tu.azzert(req.path == path)
        tu.azzert(req.query == query)
        tu.azzert(req.headers['header1'] == 'vheader1')
        tu.azzert(req.headers['header2'] == 'vheader2')
        tu.azzert(req.params['param1'] == 'vparam1')
        tu.azzert(req.params['param2'] == 'vparam2')


        headers = req.headers
        tu.azzert(headers.contains('header1'))
        tu.azzert(headers.contains('header2'))
        tu.azzert(headers.contains('header3'))
        tu.azzert(not headers.is_empty)

        headers.remove('header3')
        tu.azzert(not headers.contains('header3'))

        req.response.put_header('rheader1', 'vrheader1')
        req.response.put_header('rheader2', 'vrheader2')
        body = Buffer.create()

        @req.data_handler
        def data_handler(data):
            tu.check_thread()
            body.append_buffer(data)

        if method != 'HEAD' and method != 'CONNECT':
            req.response.chunked = chunked

        @req.end_handler
        def end_handler():
            tu.check_thread()
            if method != 'HEAD' and method != 'CONNECT':
                if not chunked:
                    req.response.put_header('Content-Length', str(body.length))
                req.response.write(body)
                if chunked:
                    req.response.put_trailer('trailer1', 'vtrailer1')
                    req.response.put_trailer('trailer2', 'vtrailer2')
            req.response.end()

    client.try_use_compression = False
    tu.azzert(client.try_use_compression == False)

    if ssl:
        client.ssl = True
        client.key_store_path = './src/test/keystores/client-keystore.jks'
        client.key_store_password = 'wibble'
        client.trust_store_path = './src/test/keystores/client-truststore.jks'
        client.trust_store_password = 'wibble'

    sent_buff = TestUtils.gen_buffer(1000)

    def response_handler(resp):
        tu.check_thread()
        tu.azzert(200 == resp.status_code)
        tu.azzert('vrheader1' == resp.headers['rheader1'])
        tu.azzert('vrheader2' == resp.headers['rheader2'])
        body = Buffer.create()
        
        @resp.data_handler
        def data_handler(data):
            tu.check_thread()
            body.append_buffer(data)

        @resp.end_handler
        def end_handler():
            tu.check_thread()
            if method != 'HEAD' and method != 'CONNECT':
                tu.azzert(TestUtils.buffers_equal(sent_buff, body))
                if chunked:
                    tu.azzert('vtrailer1' == resp.trailers['trailer1'])
                    tu.azzert('vtrailer2' == resp.trailers['trailer2'])

            resp.headers.clear()
            tu.azzert(resp.headers.is_empty)
            tu.test_complete()

    def listen_handler(err, serv):
        tu.azzert(err == None)
        tu.azzert(serv == server)
        request = client.request(method, uri, response_handler)

        request.chunked = chunked
        request.put_header('header1', 'vheader1')
        request.put_header('header2', 'vheader2')
        if not chunked:
            request.put_header('Content-Length', str(sent_buff.length))

        request.headers.add('header3', 'vheader3_1').add('header3', 'vheader3')


        size = request.headers.size
        names = request.headers.names()
        tu.azzert(size == len(names))

        for k in names:
            tu.azzert(request.headers.get_all(k) is not None)

        request.write(sent_buff)
        request.end()

    server.listen(8080, "0.0.0.0", listen_handler)


def vertx_stop():
    tu.check_thread()
    tu.unregister_all()
    client.close()
    def close_handler(err, status):
        tu.azzert(err == None)
        tu.app_stopped()
    server.close(close_handler)

tu.register_all(HttpTest())
tu.app_ready()
