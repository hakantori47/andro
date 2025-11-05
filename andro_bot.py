import requests
import re
import datetime

def get_DeaTHLesS_streams():
    print("🔍 Searching for active domain...")
    
    # Domain bulma
    active_domain = None
    for i in range(42, 100):
        url = f"https://birazcikspor{i}.xyz/"
        try:
            response = requests.head(url, timeout=3)
            if response.status_code == 200:
                active_domain = url
                print(f"✅ Found: {active_domain}")
                break
        except:
            continue
    
    if not active_domain:
        print("❌ No active domain found")
        return ""
    
    # HTML al
    try:
        response = requests.get(active_domain, timeout=10)
        html = response.text
    except:
        print("❌ Cannot access main page")
        return ""
    
    # Iframe ID bul
    first_id_match = re.search(r'<iframe[^>]+id="matchPlayer"[^>]+src="event\.html\?id=([^"]+)"', html)
    if not first_id_match:
        print("❌ No iframe ID found")
        return ""
    
    first_id = first_id_match.group(1)
    
    # Base URL al
    base_url = ""
    try:
        event_response = requests.get(f"{active_domain}event.html?id={first_id}", timeout=10)
        event_source = event_response.text
        base_url_match = re.search(r'var\s+baseurls\s*=\s*\[\s*"([^"]+)"', event_source)
        if base_url_match:
            base_url = base_url_match.group(1)
            print(f"🌐 Base URL: {base_url}")
        else:
            print("❌ Base URL not found")
            return ""
    except:
        print("❌ Cannot get base URL")
        return ""
    
    # TÜM KANALLAR - EKSİKSİZ LİSTE
    channels = [
        ["beIN Sport 1 HD", "androstreamlivebs1"],
        ["beIN Sport 2 HD", "androstreamlivebs2"],
        ["beIN Sport 3 HD", "androstreamlivebs3"],
        ["beIN Sport 4 HD", "androstreamlivebs4"],
        ["beIN Sport 5 HD", "androstreamlivebs5"],
        ["beIN Sport Max 1 HD", "androstreamlivebsm1"],
        ["beIN Sport Max 2 HD", "androstreamlivebsm2"],
        ["S Sport 1 HD", "androstreamlivess1"],
        ["S Sport 2 HD", "androstreamlivess2"],
        ["Tivibu Sport HD", "androstreamlivets"],
        ["Tivibu Sport 1 HD", "androstreamlivets1"],
        ["Tivibu Sport 2 HD", "androstreamlivets2"],
        ["Tivibu Sport 3 HD", "androstreamlivets3"],
        ["Tivibu Sport 4 HD", "androstreamlivets4"],
        ["Smart Sport 1 HD", "androstreamlivesm1"],
        ["Smart Sport 2 HD", "androstreamlivesm2"],
        ["Euro Sport 1 HD", "androstreamlivees1"],
        ["Euro Sport 2 HD", "androstreamlivees2"],
        ["Tabii HD", "androstreamlivetb"],
        ["Tabii 1 HD", "androstreamlivetb1"],
        ["Tabii 2 HD", "androstreamlivetb2"],
        ["Tabii 3 HD", "androstreamlivetb3"],
        ["Tabii 4 HD", "androstreamlivetb4"],
        ["Tabii 5 HD", "androstreamlivetb5"],
        ["Tabii 6 HD", "androstreamlivetb6"],
        ["Tabii 7 HD", "androstreamlivetb7"],
        ["Tabii 8 HD", "androstreamlivetb8"],
        ["Exxen HD", "androstreamliveexn"],
        ["Exxen 1 HD", "androstreamliveexn1"],
        ["Exxen 2 HD", "androstreamliveexn2"],
        ["Exxen 3 HD", "androstreamliveexn3"],
        ["Exxen 4 HD", "androstreamliveexn4"],
        ["Exxen 5 HD", "androstreamliveexn5"],
        ["Exxen 6 HD", "androstreamliveexn6"],
        ["Exxen 7 HD", "androstreamliveexn7"],
        ["Exxen 8 HD", "androstreamliveexn8"],
    ]
    
    print(f"📡 Checking {len(channels)} channels...")
    m3u_content = "#EXTM3U\n"
    working_channels = 0
    
    for name, code in channels:
        stream_url = f"{base_url}{code}.m3u8"
        try:
            response = requests.head(stream_url, timeout=3)
            if response.status_code == 200:
                m3u_content += f'#EXTINF:-1 tvg-id="{code}" tvg-name="TR:{name}" tvg-logo="https://i.hizliresim.com/8xzjgqv.jpg" group-title="SPORT",TR:{name}\n'
                m3u_content += f"{stream_url}\n"
                working_channels += 1
                print(f"✅ {name}")
            else:
                print(f"❌ {name}")
        except:
            print(f"❌ {name}")
    
    print(f"🎯 {working_channels}/{len(channels)} channels working")
    
    if working_channels == 0:
        return ""
    
    return m3u_content

if __name__ == "__main__":
    print("🚀 DeaTHLesS Bot Starting...")
    result = get_DeaTHLesS_streams()
    
    if result:
        with open("DeaTHlesS-Androiptv.m3u", "w", encoding="utf-8") as f:
            f.write(result)
        print("💾 M3U file created successfully!")
    else:
        print("💥 Failed to create M3U file")
