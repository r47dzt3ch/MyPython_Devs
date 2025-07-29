import requests
import json

url = "https://dolphin-anty-api.com/browser_profiles"
# Residential Proxy Credentials
PROXY_HOST = "res.proxy-seller.com"
PROXY_PORT = "10275"
PROXY_USERNAME = "5f1d6a36763c82af"
PROXY_PASSWORD = "1yhfUOBk"
payload = json.dumps({
    "name": "Test",
    "tags": ["Test"],
    "platform": "macos",
    "browserType": "anty",
    "mainWebsite": "",
    "useragent": {
        "mode": "manual",
        "value": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    },
    "webrtc": {
        "mode": "altered",
        "ipAddress": None
    },
    "canvas": {
        "mode": "real"
    },
    "webgl": {
        "mode": "real"
    },
    "webglInfo": {
        "mode": "manual",
        "vendor": "Google Inc. (Apple)",
        "renderer": "ANGLE (Apple, Apple M1 Max, OpenGL 4.1)",
        "webgl2Maximum": "{\"UNIFORM_BUFFER_OFFSET_ALIGNMENT\":256,\"MAX_TEXTURE_SIZE\":16384,\"MAX_VIEWPORT_DIMS\":[16384,16384],\"MAX_VERTEX_ATTRIBS\":16,\"MAX_VERTEX_UNIFORM_VECTORS\":1024,\"MAX_VARYING_VECTORS\":31,\"MAX_COMBINED_TEXTURE_IMAGE_UNITS\":32,\"MAX_VERTEX_TEXTURE_IMAGE_UNITS\":16,\"MAX_TEXTURE_IMAGE_UNITS\":16,\"MAX_FRAGMENT_UNIFORM_VECTORS\":1024,\"MAX_CUBE_MAP_TEXTURE_SIZE\":16384,\"MAX_RENDERBUFFER_SIZE\":16384,\"MAX_3D_TEXTURE_SIZE\":2048,\"MAX_ELEMENTS_VERTICES\":1048575,\"MAX_ELEMENTS_INDICES\":150000,\"MAX_TEXTURE_LOD_BIAS\":16,\"MAX_DRAW_BUFFERS\":8,\"MAX_FRAGMENT_UNIFORM_COMPONENTS\":4096,\"MAX_VERTEX_UNIFORM_COMPONENTS\":4096,\"MAX_ARRAY_TEXTURE_LAYERS\":2048,\"MIN_PROGRAM_TEXEL_OFFSET\":-8,\"MAX_PROGRAM_TEXEL_OFFSET\":7,\"MAX_VARYING_COMPONENTS\":124,\"MAX_TRANSFORM_FEEDBACK_SEPARATE_COMPONENTS\":4,\"MAX_TRANSFORM_FEEDBACK_INTERLEAVED_COMPONENTS\":64,\"MAX_TRANSFORM_FEEDBACK_SEPARATE_ATTRIBS\":4,\"MAX_COLOR_ATTACHMENTS\":8,\"MAX_SAMPLES\":4,\"MAX_VERTEX_OUTPUT_COMPONENTS\":64,\"MAX_FRAGMENT_INPUT_COMPONENTS\":128,\"MAX_ELEMENT_INDEX\":4294967295}"
    },
    "webgpu": {
        "mode": "manual"
    },
    "clientRect": {
        "mode": "real"
    },
    "notes": {
        "content": None,
        "color": "blue",
        "style": "text",
        "icon": "info"
    },
    "timezone": {
        "mode": "auto",
        "value": None
    },
    "locale": {
        "mode": "auto",
        "value": None
    },

    "statusId": 0,
    "geolocation": {
        "mode": "auto",
        "latitude": None,
        "longitude": None,
        "accuracy": None
    },
    "cpu": {
        "mode": "manual",
        "value": 8
    },
    "memory": {
        "mode": "manual",
        "value": 8
    },
    "screen": {
        "mode": "real",
        "resolution": None
    },
    "audio": {
        "mode": "real"
    },
    "mediaDevices": {
        "mode": "real",
        "audioInputs": None,
        "videoInputs": None,
        "audioOutputs": None
    },
    "ports": {
        "mode": "protect",
        "blacklist": "3389,5900,5800,7070,6568,5938"
    },
    "doNotTrack": False,
    "args": [],
    "platformVersion": "13.4.1",
    "uaFullVersion": "120.0.5845.96",
    "login": "",
    "password": "",
    "appCodeName": "Mozilla",
    "platformName": "MacIntel",
    "connectionDownlink": 2.05,
    "connectionEffectiveType": "4g",
    "connectionRtt": 150,
    "connectionSaveData": 0,
    "cpuArchitecture": "",
    "osVersion": "10.15.7",
    "vendorSub": "",
    "productSub": "20030107",
    "vendor": "Google Inc.",
    "product": "Gecko",
    "proxy": {
        "type": "socks5",
        "host": PROXY_HOST,
        "port": PROXY_PORT,
        "login": PROXY_USERNAME,
        "password": PROXY_PASSWORD,
        "name": f"socks5://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}",
        "changeIpUrl": "",
    },
})

headers = {
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMGNjNGU0MjNhMGFmN2U2OTc3MDEzM2RlNmQ0ZTY4MGIxNmY1ZTQ3ZTk5OTU3YTVjMGE1MjBhMzYxOWViYmYzZGQ3MDJmNmYxMTFmYzBiM2MiLCJpYXQiOjE3NTM3NTU5ODkuODU4NzE4LCJuYmYiOjE3NTM3NTU5ODkuODU4NzIxLCJleHAiOjE3NjE1MzE5ODkuODUwNzI4LCJzdWIiOiI0NTUxODk1Iiwic2NvcGVzIjpbXSwidGVhbV9pZCI6NDAzNjg0MCwidGVhbV9wbGFuIjoiZW50ZXJwcmlzZSIsInRlYW1fcGxhbl9leHBpcmF0aW9uIjoxNzU1OTE3ODkzfQ.W21dscrzq-ksqhcjjCegf4UHF3DmfZI4ZndpyGN7lDnw2qar_aAyRKwA3aaN8fFZwRho5SBmbZqwDE7CKUS2BMZZhClCzNW1LX9EuH_ZZcdXern3VBY4PRaSlKr0r9YfhyOTbfj4CeXntzKZlxINE9Z55SYxEryg2ej1Yl4SJ2MZeJvOzFekwEVkwWYQvtgc_Mb-BvIbSqfl2BFAo6rhduPJL7D0MyVTxqjME_nuAbEFI3DHvEilBZSYGg-Ersn_buswGWLSeqN7dQmnZx8aLrSKRdc_sacYm3Dp7MQwstRAhZisCzbGSxX5X2hIKz733QJxcLPCHE2dmwBOpg6CvJNCOZRwx5hoe5iQHxMvkzI91s4A7XUX4u_4WL6z1QlZit9JMHQg0Z1jR09N-CNHzWiJBDd8iW7nRbBBaTM24LuR100QboYwV0rFsQCr9mBR5oHfze0BTQq5vgX_byBuQRJAJOu8AYumuc6Jix5QiaTxN529WJ88RIv5iPI4PvflvdIHsFhxDEBDU1DLe5weyuJ-g1eq0V-CXfBkIGH8L2UJiCCvIFFbBAI_G-iwW8o_DJf2gP_t5P21PGn7BoHYuP3c17Cwxb3sK8BwA4AfYOeD1Mu_gP_r0_InGNGyJQEB_M8UdZIHk6Pa7dl0ica6ONTjLOA8wKt3pfmkDAa6SyA',
    'content-type': 'application/json',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

