import json,base64,urllib.request,pathlib
img=base64.b64encode(pathlib.Path('../../entry/entry.png').read_bytes()).decode()
prompt=("Deskripsi gambar 1024x1024 ini apa adanya: sebut teks judul terbesar, jumlah panel, apakah ada teks tumpang tindih/terpotong, elemen yang tampak rusak, dan 3 saran perbaikan konkret. Ringkas, bahasa Indonesia.")
for m in ["gemini/gemini-3-flash","gemini/gemini-2.5-flash","sf/step-5-preview","gpt-5.4","claude-3-7-sonnet"]:
    body={"model":m,"max_tokens":500,"messages":[{"role":"user","content":[{"type":"text","text":prompt},{"type":"image_url","image_url":{"url":"data:image/png;base64,"+img}}]}]}
    r=urllib.request.Request("http://127.0.0.1:20128/v1/chat/completions",data=json.dumps(body).encode(),headers={"content-type":"application/json"})
    try:
        d=json.load(urllib.request.urlopen(r,timeout=120))
        c=d["choices"][0]["message"].get("content")
        print("==",m,"OK len",len(c or ""))
        print((c or "")[:900]); break
    except Exception as e:
        print("==",m,"ERR",getattr(e,'code',None),getattr(e,'read',lambda:b'')()[:120])
