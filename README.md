# ARP Detection Script

This script is written in Python and designed to detect network anomalies, specifically excessive ARP request activities. It is intended to run on Linux-based devices such as Raspberry Pi and utilizes several Python libraries, including `subprocess`, `asyncio`, and `re`.

By executing the tcpdump command, the script asynchronously monitors ARP traffic and applies regex patterns to detect excessive ARP requests from specific IP addresses. If the number of ARP requests from an IP address exceeds a defined threshold within a certain time frame, the script flags it as a potential attack.

Detected anomalies are then sent in real-time to a Discord channel using a bot connected through the Discord API. A message rate-limiting mechanism is also implemented to prevent spam.

This approach enables network administrators to receive immediate notifications when suspicious activities are detected on their network.

---
Topology: 

![Diagram ARP Detection](topology_example.jpg)

---
## Catatan
- Make sure that devices are on the same network.
- Do the test using `Nmap` or other testing tools.