import requests

def ping_server():
    url = "https://techbay-1ej5.onrender.com"   # replace with your real backend URL
    try:
        requests.get(url, timeout=10)
        print("Pinged successfully!")
    except Exception as e:
        print("Ping failed:", e)

if __name__ == "__main__":
    ping_server()
