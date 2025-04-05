import subprocess
import re
import asyncio
from collections import defaultdict
import discord

# Pola regex untuk mendeteksi ARP request
arp_pattern = re.compile(
    r"(?P<time>\d{2}:\d{2}:\d{2}\.\d{6}) ARP, Request who-has "
    r"(?P<target_ip>\d+\.\d+\.\d+\.\d+) tell (?P<source_ip>\d+\.\d+\.\d+\.\d+), length \d+"
)

# Ambang batas deteksi anomali
THRESHOLD = 10
TIME_WINDOW = 1  # dalam detik
MESSAGE_LIMIT = 3  # Batas pengiriman pesan

# Dictionary untuk menyimpan status request
arp_requests_count = defaultdict(int)
last_request_time = defaultdict(float)

# Konfigurasi Discord
TOKEN = 'PASTE_YOUR_DISCORD_TOKEN_HERE'
CHANNEL_ID = xxxx


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_count = defaultdict(int)
        self.last_send_time = defaultdict(float)
        self.anomaly_detected = defaultdict(bool)

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        asyncio.create_task(self.monitor_arp())

    async def send_anomaly_alert(self, source_ip):
        channel = self.get_channel(CHANNEL_ID)
        if self.message_count[source_ip] < MESSAGE_LIMIT:
            await channel.send(f"⚠️ Anomaly detected: Excessive ARP requests from {source_ip}")
            self.message_count[source_ip] += 1
            self.last_send_time[source_ip] = asyncio.get_event_loop().time()
            print(f"Sent {self.message_count[source_ip]} anomaly alert(s) for IP {source_ip}.")

    async def monitor_arp(self):
        try:
            process = await asyncio.create_subprocess_exec(
                'tcpdump', '-l', '-n', 'arp',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            print("Monitoring ARP traffic for anomaly detection...")

            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                line = line.decode('utf-8').strip()
                match = arp_pattern.match(line)
                if match:
                    source_ip = match.group('source_ip')
                    current_time = asyncio.get_event_loop().time()

                    # Reset count jika melewati time window
                    if current_time - last_request_time[source_ip] > TIME_WINDOW:
                        arp_requests_count[source_ip] = 0
                        last_request_time[source_ip] = current_time

                    arp_requests_count[source_ip] += 1

                    # Deteksi jika ada ARP scan berlebih
                    if arp_requests_count[source_ip] > THRESHOLD:
                        if not self.anomaly_detected[source_ip]:
                            self.anomaly_detected[source_ip] = True
                            await self.send_anomaly_alert(source_ip)
                    else:
                        # Reset setelah 2 menit
                        if current_time - self.last_send_time[source_ip] >= 120:
                            self.message_count[source_ip] = 0
                            self.anomaly_detected[source_ip] = False

        except asyncio.CancelledError:
            print("Task was cancelled.")
            process.terminate()
            await process.wait()


# Mulai client Discord
intents = discord.Intents.default()
client = MyClient(intents=intents)
client.run(TOKEN)
