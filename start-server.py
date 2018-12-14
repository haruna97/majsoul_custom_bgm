import http.client
import http.server
import socketserver
import json
import os, re

try:
	c = http.client.HTTPSConnection("majsoul.union-game.com", timeout=2)

	print('get latest version info... ', end='')
	c.request('GET', '/0/version.json')
	r = c.getresponse()
	print('%s %s' % (r.status, r.reason))
	a = r.read().decode('utf-8')
	a = json.loads(a)
	print('latest game version is:%s' % re.match(r'(v.*?)/.*?\.js', a['code']).group(1))

	print('get code.js... ', end='')
	c.request('GET', '/0/'+a['code'])
	r = c.getresponse()
	print('%s %s' % (r.status, r.reason))
	a = r.read().decode('utf-8')

	print('patching...')
	a += open('bgm.js', 'r', encoding='utf8').read()

	if not os.path.exists('web'):
		os.makedirs('web')
	open('web/code.patched.js', 'w', encoding='utf8').write(a)

	print('done.\n')
	print('starting http server...')

	web_dir = os.path.join(os.path.dirname(__file__), 'web')
	os.chdir(web_dir)

	PORT = 8000
	Handler = http.server.SimpleHTTPRequestHandler
	httpd = socketserver.TCPServer(("", PORT), Handler)
	print("http.server serving at port", PORT)
	httpd.serve_forever()

except Exception as e:
	print(e.message if hasattr(e, 'message') else e)
	print('\nerror occurred, please try again.')
	os.system("pause")
