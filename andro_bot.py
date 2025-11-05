import requests
import re
import os
import datetime

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
        return ""
    
    try:
        response = requests.get(active_domain, timeout=10)
        html = response.text
    except:
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
        return ""
    
    channels = [
        ["beIN Sport 1 HD", "androstreamlivebs1", "https://i.hizliresim.com/8xzjgqv.jpg"],
        ["beIN Sport 2 HD", "androstreamlivebs2", "https://i.hizliresim.com/8xzjgqv.jpg"],
        # ... tüm kanallar buraya
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
        except:
            continue
    
    m3u_header = f"""#EXTM3U
# Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Total Channels: {len(successful_channels)}
# GitHub: https://github.com/hakantori47/andro-iptv

"""
    
    return m3u_header + m3u_content

def save_m3u_file(content):
    os.makedirs("docs", exist_ok=True)
    file_path = "docs/DeaTHlesS-Androiptv.m3u"
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        return False

if __name__ == "__main__":
    m3u_data = get_DeaTHLesS_streams()
    if m3u_data:
        save_m3u_file(m3u_data)
