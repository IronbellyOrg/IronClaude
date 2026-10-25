import re
def sig(e):
    p=[]
    if "error_type" in e: p.append(e["error_type"])
    if "error_message" in e: p.append(re.sub(r"\d+","N",e["error_message"])[:100])
    if "test_name" in e: p.append(e["test_name"])
    return " | ".join(p)
def ratio(a,b):
    w1,w2=set(sig(a).lower().split()),set(sig(b).lower().split())
    return len(w1&w2),len(w1|w2),len(w1&w2)/len(w1|w2)
# message-only JWT example from old guide
print("jwt msg-only", len(set("jwt token validation failed missing secret".split())&set("jwt validation failed secret not found".split())), len(set("jwt token validation failed missing secret".split())|set("jwt validation failed secret not found".split())))
stored={"error_type":"ValueError","error_message":"invalid port value 8080 in config","test_name":"test_load_config"}
cur_hi={"error_type":"ValueError","error_message":"invalid port value 9090 in config file","test_name":"test_load_config"}
cur_lo={"error_type":"ValueError","error_message":"invalid timeout value 30 in settings","test_name":"test_load_settings"}
print(sig(stored)); print(sig(cur_hi)); print(ratio(cur_hi,stored)); print(ratio(cur_lo,stored))

# attempt 4: third pair (message-only JWT) and summary of all three guide examples
pairs = [
    ({"error_type": "ValueError", "error_message": "invalid port value 8080 in config", "test_name": "test_load_config"},
     {"error_type": "ValueError", "error_message": "invalid port value 9090 in config file", "test_name": "test_load_config"}),
    ({"error_type": "ValueError", "error_message": "invalid port value 8080 in config", "test_name": "test_load_config"},
     {"error_type": "ValueError", "error_message": "invalid timeout value 30 in settings", "test_name": "test_load_settings"}),
    ({"error_message": "JWT validation failed secret not found"},
     {"error_message": "JWT token validation failed missing secret"}),
]
for a, b in pairs:
    print("guide pair", ratio(b, a))

# attempt 5: the exactly-0.70 boundary pair now in the guide
print("boundary pair", ratio(
    {"error_type": "ValueError", "error_message": "port value 9090 in settings", "test_name": "test_load_config"},
    {"error_type": "ValueError", "error_message": "invalid port value 8080 in config", "test_name": "test_load_config"}))
