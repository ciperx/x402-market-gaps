import json,urllib.request,urllib.error,concurrent.futures,time
UA={"user-agent":"x402-truth-check/1.0","accept":"application/json"}
def get(u,t=15):
    r=urllib.request.Request(u,headers=UA)
    with urllib.request.urlopen(r,timeout=t) as f: return f.getcode(),f.read()[:200000]
def probe(svc):
    url=svc.get("url"); adv=svc.get("price_usd")
    out={"id":svc.get("id"),"name":svc.get("name"),"url":url,"advertised_usd":adv,"status":None,"live_usd":None,"verdict":None,"note":""}
    if not url: out["verdict"]="NO_URL"; return out
    for method in ("POST","GET"):
        try:
            req=urllib.request.Request(url,data=b"{}" if method=="POST" else None,headers={**UA,"content-type":"application/json"},method=method)
            try:
                with urllib.request.urlopen(req,timeout=15) as f:
                    out["status"]=f.getcode(); out["verdict"]="NO_PAYWALL" if f.getcode()<400 else "HTTP_%d"%f.getcode()
                    return out
            except urllib.error.HTTPError as e:
                out["status"]=e.code
                body=e.read()[:20000].decode("utf8","replace")
                if e.code==402:
                    try:
                        j=json.loads(body)
                    except Exception:
                        out["verdict"]="402_UNPARSEABLE"; return out
                    acc=(j.get("accepts") or [{}])[0]
                    amt=acc.get("maxAmountRequired") or acc.get("amount") or (acc.get("price") or {}).get("amount")
                    if amt is not None:
                        try: out["live_usd"]=round(int(amt)/1e6,6)
                        except Exception: out["live_usd"]=amt
                    if out["live_usd"] is not None and adv is not None:
                        ratio=(out["live_usd"]/adv) if adv else None
                        if ratio and abs(ratio-1)<0.01: out["verdict"]="MATCH"
                        elif ratio and ratio>=2: out["verdict"]="LIVE_%dx_HIGHER"%round(ratio,1)
                        elif ratio and ratio<=0.5: out["verdict"]="LIVE_CHEAPER"
                        else: out["verdict"]="DIFFERENT"
                    else: out["verdict"]="402_NO_AMOUNT"
                    return out
                out["verdict"]="HTTP_%d"%e.code; return out
        except Exception as e:
            out["note"]=str(e)[:80]; out["verdict"]=out["verdict"] or "UNREACHABLE"
    return out
def main():
    d=json.load(urllib.request.urlopen(urllib.request.Request("https://402index.io/api/v1/services?limit=100&offset=0",headers=UA),timeout=30))
    svcs=d["services"]
    # prefer self-registered-ish entries with a price
    svcs=[s for s in svcs if s.get("price_usd") and s.get("url")][:60]
    res=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for r in ex.map(probe,svcs): res.append(r)
    json.dump(res,open("sample.json","w"),indent=1)
    import collections
    print(collections.Counter(r["verdict"] for r in res).most_common())
    for r in res: print(f'{r["verdict"]:18} adv={r["advertised_usd"]} live={r["live_usd"]} {r["name"][:40] if r["name"] else ""}')
main()
