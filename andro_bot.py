import requests
import re
import os

def get_DeaTHLesS_streams():
    m3u_content = ""
    
    active_domain = None
    for i in range(42, 200):
        url = f"https://birazcikspor{i}.xyz/"
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                active_domain = url
                break
        except:
            continue
    
    if not active_domain:
        print("<!-- Birazcikspor: No active domain found -->")
        return ""
    
    try:
        response = requests.get(active_domain, timeout=10)
        html = response.text
    except:
        print("<!-- Birazcikspor: Main page not accessible -->")
        return ""
    
    first_id_match = re.search(r'<iframe[^>]+id="matchPlayer"[^>]+src="event\.html\?id=([^"]+)"', html)
    first_id = first_id_match.group(1) if first_id_match else None
    
    base_url = ""
    if first_id:
        try:
            event_response = requests.get(f"{active_domain}event.html?id={first_id}", timeout=10)
            event_source = event_response.text
            base_url_match = re.search(r'var\s+baseurls\s*=\s*\[\s*"([^"]+)"', event_source)
            base_url = base_url_match.group(1) if base_url_match else ""
        except:
            pass
    
    if not base_url:
        print("<!-- Birazcikspor: Base URL not found -->")
        return ""
    
    channels = [
        ["beIN Sport 1 HD", "androstreamlivebs1", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["beIN Sport 2 HD", "androstreamlivebs2", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["beIN Sport 3 HD", "androstreamlivebs3", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["beIN Sport 4 HD", "androstreamlivebs4", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["beIN Sport 5 HD", "androstreamlivebs5", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["beIN Sport Max 1 HD", "androstreamlivebsm1", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["beIN Sport Max 2 HD", "androstreamlivebsm2", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["S Sport 1 HD", "androstreamlivess1", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["S Sport 2 HD", "androstreamlivess2", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Tivibu Sport HD", "androstreamlivets", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Tivibu Sport 1 HD", "androstreamlivets1", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Tivibu Sport 2 HD", "androstreamlivets2", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Tivibu Sport 3 HD", "androstreamlivets3", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Tivibu Sport 4 HD", "androstreamlivets4", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Smart Sport 1 HD", "androstreamlivesm1", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Smart Sport 2 HD", "androstreamlivesm2", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Euro Sport 1 HD", "androstreamlivees1", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Euro Sport 2 HD", "androstreamlivees2", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Tabii HD", "androstreamlivetb", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Tabii 1 HD", "androstreamlivetb1", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Tabii 2 HD", "androstreamlivetb2", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Tabii 3 HD", "androstreamlivetb3", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Tabii 4 HD", "androstreamlivetb4", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Tabii 5 HD", "androstreamlivetb5", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Tabii 6 HD", "androstreamlivetb6", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Tabii 7 HD", "androstreamlivetb7", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Tabii 8 HD", "androstreamlivetb8", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Exxen HD", "androstreamliveexn", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Exxen 1 HD", "androstreamliveexn1", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Exxen 2 HD", "androstreamliveexn2", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Exxen 3 HD", "androstreamliveexn3", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Exxen 4 HD", "androstreamliveexn4", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Exxen 5 HD", "androstreamliveexn5", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Exxen 6 HD", "androstreamliveexn6", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Exxen 7 HD", "androstreamliveexn7", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["Exxen 8 HD", "androstreamliveexn8", "https://i.hizliresim.com/8xzjgqv.jpg"],
    ]
    
    successful_channels = []
    
    for channel in channels:
        stream_url = f"{base_url}{channel[1]}.m3u8"
        try:
            response = requests.head(stream_url, timeout=5)
            if response.status_code == 200:
                m3u_content += f'#EXTINF:-1 tvg-id="sport.tr" tvg-name="TR:{channel[0]}" tvg-logo="{channel[2]}" group-title="TURKIYE DEATHLESS",TR:{channel[0]}\n'
                m3u_content += f"{stream_url}\n"
                successful_channels.append(channel[0])
                print(f"✅ {channel[0]}")
            else:
                print(f"❌ {channel[0]}")
        except:
            print(f"❌ {channel[0]}")
