# GetHeader

250 points (medium)
Leaders are the head of the team.
Link: http://138.68.36.145/
Author: Vidhun

---

Upon navigating the provided URL `http://138.68.36.145/`, we get raw JSON

```json
{
  "Endpoints": [
    [
      "/source",
      {
        "Method": "GET",
        "Param": {
          "type": "bool",
          "value": "view"
        }
      }
    ],
    [
      "/getHeader",
      {
        "Example": {
          "Request": "url=http://example.com",
          "Response": {
            "Accept-Ranges": "bytes",
            "Age": "349563",
            "Cache-Control": "max-age=604800",
            "Content-Encoding": "gzip",
            "Content-Length": "648",
            "Content-Type": "text/html; charset=UTF-8",
            "Date": "Tue, 06 Oct 2020 09:37:06 GMT",
            "Etag": "3147526947",
            "Expires": "Tue, 13 Oct 2020 09:37:06 GMT",
            "Last-Modified": "Thu, 17 Oct 2019 07:18:26 GMT",
            "Server": "ECS (oxr/832D)",
            "Vary": "Accept-Encoding",
            "X-Cache": "HIT"
          }
        },
        "Method": "POST",
        "Param": {
          "type": "string",
          "value": "url"
        }
      }
    ]
  ]
}
```

We see 2 endpoints: `/source` & `/getHeader`, where `/source` expects a `GET` request with a boolean value `view` and `/getHeader` expects a `POST` request with a string value `url`.

First, we check `http://138.68.36.145/source?view=true`

```python
from flask.json import jsonify
   import requests, re
   from flask import Flask, request, make_response,  render_template
   app = Flask(__name__)

   regex = re.compile(r'^((?:http(?:s)?:\/\/)?)((?:www\.)?[a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b)((?:\:\d+)?)((?:[-\w@:%\+.~#&/=]*)?)((?:\?[-\w%\+.~#&=]*)?)$', re.IGNORECASE)


   @app.route('/', methods=['GET'])
   def index():
       return jsonify({"Endpoints":[["/source",{"Method":"GET","Param":{"value":"view","type":"bool"}}],["/getHeader",{"Method":"POST","Param":{"value":"url","type":"string"},"Example":{"Request":"url=http://example.com","Response":{"Content-Encoding":"gzip","Accept-Ranges":"bytes","Age":"349563","Cache-Control":"max-age=604800","Content-Type":"text/html; charset=UTF-8","Date":"Tue, 06 Oct 2020 09:37:06 GMT","Etag":"3147526947","Expires":"Tue, 13 Oct 2020 09:37:06 GMT","Last-Modified":"Thu, 17 Oct 2019 07:18:26 GMT","Server":"ECS (oxr/832D)","Vary":"Accept-Encoding","X-Cache":"HIT","Content-Length":"648"}}}]]}),200


   @app.route('/getHeader', methods=['POST'])
   def header():
       if request.form.get('url'):
           url = request.form.get('url')
           if re.match(regex, url):
               res = requests.get(url,allow_redirects=True)
               return jsonify(dict(res.headers)),200
           else:
               return jsonify({"error":"Given input is not url"}),200
       else:
           return jsonify({"error":"Something Went Wrong!"}),200

   @app.route('/source', methods=['GET'])
   def source():
       if request.args.get('view'):
           value = request.args.get('view')
           if(value=="true"):
               return render_template('source.html')
           else:
               return '',201
       else:
           return '',201


   if __name__ == '__main__':
       app.run(host='127.0.0.1', port=80)
```

The URL gives us the source code for the page `source.html`. Note that when we go to `view-source:http://138.68.36.145/source?view=true`, there's an HTML comment at the bottom: `<!--Grab the flag from :8080-->`. However, there doesn't seem to be anything at `http://138.68.36.145:8080/`, and an `nmap 138.68.36.145 -p 8080` scan shows that the port 8080 is closed.

As we can see, `/` simple returns some hard-coded JSON data, `/source` returns the source code `source.html` when `view` is set to `true`, and `/getHeader` checks the `POST` request for a form submission in which the value of `url` is checked against `regex`. Note that the variable `url` is retrieved with `request.form.get('url')`, meaning the `url` needs to be passed as a form, rather than a parameter in the URL as `/getHeader?url=some_url`. If we don't correctly pass in a `url` in a form, we get the reply `{"error":"Something Went Wrong!"}`. First, I'll try passing `http://example.com` as `url` (`jq` parses JSON for the command line)

```sh
$ curl -s -X POST http://138.68.36.145/getHeader -F "url=http%3A%2F%2F138.68.36.145%2F"
{"error":"Given input is not url"}

# Passing a URL-encoded URL returns the "is not url" error .Since this is not passed in the URL, the data doesn't get URL-decoded

$ curl -s -X POST http://138.68.36.145/getHeader -F "url=http://example.com" | jq

{
  "Age": "401586",
  "Cache-Control": "max-age=604800",
  "Content-Encoding": "gzip",
  "Content-Length": "648",
  "Content-Type": "text/html; charset=UTF-8",
  "Date": "Sat, 31 Oct 2020 06:37:22 GMT",
  "Etag": "\"3147526947+gzip\"",
  "Expires": "Sat, 07 Nov 2020 08:36:22 GMT",
  "Last-Modified": "Thu, 17 Oct 2019 07:17:26 GMT",
  "Server": "ECS (sjc/4E76)",
  "Vary": "Accept-Encoding",
  "X-Cache": "HIT"
}
```

Since we passed in the URL correctly, we got some headers as said in the source code, but how should we use the headers? The source code doesn't seem to have anything to check specific headers.

Since we've got the headers, I tried using the returned headers in a request to maybe get the flag which supposedly is at `:8080`.

```python
#!/usr/bin/python3

import requests
import json

# POST /getHeader

url = "http://138.68.36.145/getHeader"
data = {"url": "http://example.com"}
r_getHeader = requests.post(url, data=data)
print(r_getHeader.text)

# Get flag at :8080

url = "http://138.68.36.145:8080"
headers = json.loads(r_getHeader.text)
r = requests.post(url, headers=headers)
print(r.text)
```

However, this didn't work. As I took a look back at `source.html`, I realized that the headers we got back are the response headers from `example.com`, which you can get by trying `curl -I http://example.com`. Since this is returning the response headers from requests made by the server, and the port 8080 which is supposed to have the flag if we believe the HTML comments is closed, I got the idea to have the server make a request to itself on port 8080, which might be closed to us but open to the internal server.

```sh
$ curl -s -X POST http://138.68.36.145/getHeader -F "url=http://localhost:8080"
{"error":"Given input is not url"}

$ curl -s -X POST http://138.68.36.145/getHeader -F "url=http://127.0.0.1:8080"
{"error":"Given input is not url"}

$ curl -s -X POST http://138.68.36.145/getHeader -F "url=http://2130706433:8080" # integer form of 127.0.0.1
{"error":"Given input is not url"}

$ curl -s -X POST http://138.68.36.145/getHeader -F "url=http://0x7f000001:8080" # hex form of 127.0.0.1
{"error":"Given input is not url"}

$ curl -s -X POST http://138.68.36.145/getHeader -F "url=http://0:8080" # try `ping 0`
{"error":"Given input is not url"}
```

My totally legitimate URLs aren't considered URLS?! Who wrote the regex?!

Let's look back at the URL regex...

```
^((?:http(?:s)?:\/\/)?)((?:www\.)?[a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b)((?:\:\d+)?)((?:[-\w@:%\+.~#&/=]*)?)((?:\?[-\w%\+.~#&=]*)?)$

^((?:http(?:s)?:\/\/)?)((?:www\.)?                                          )((?:\:\d+)?)((?:[-\w@:%\+.~#&/=]*)?)((?:\?[-\w%\+.~#&=]*)?)$
                                  [a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b
                                                            ^
                                                          problem
```

After staring at someone else's regex & testing, I've found that the problem likely lies in the piece `\.[a-z]{2,6}\b`, which requires a `AA.BB` in the part between `http://` & the port `:8080`, where `AA` is a string of length 2-256, and `BB` is a string of length 2-6, and `BB` has to be lowercase letters. This means `localhost.aa` and `127.0.0.1.aa` would work, except they're not valid URLs for `localhost`. This means I need some TLD (e.g. `.com`, `.org`) after `localhost` and `127.0.0.1`. To get a valid URL, I tried `nslookup` and `dig`

```sh
$ nslookup 138.68.36.145
** server can't find 145.36.68.138.in-addr.arpa: NXDOMAIN

$ dig 138.68.36.145 A

; <<>> DiG 9.16.6 <<>> 138.68.36.145 A
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 3444
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;138.68.36.145.			IN	A

;; AUTHORITY SECTION:
.			422	IN	SOA	a.root-servers.net. nstld.verisign-grs.com. 2020103100 1800 900 604800 86400

;; Query time: 3 msec
;; SERVER: 123.23.23.23#53(123.23.23.23)
;; WHEN: Sat Oct 31 17:42:51 +06 2020
;; MSG SIZE  rcvd: 117
```

Unfortunately, DNS doesn't work. There's also no sign of an acceptable URL in `source.html`. I then also tried the domain `yetanothersec.com`

```sh
$ curl -s -X POST http://138.68.36.145/getHeader -F "url=https://ctf.yetanothersec.com"
$ curl -s -X POST http://138.68.36.145/getHeader -F "url=https://yetanothersec.com"
$ curl -s -X POST http://138.68.36.145/getHeader -F "url=https://ctf.yetanothersec.com/challenges#GetHeader-4"
```

None of which returns anything useful.

Unfortunately, the competition ended before I could finish testing this, so I'll leave others to present the final solution to this problem.
