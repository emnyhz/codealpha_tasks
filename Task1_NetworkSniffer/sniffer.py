from datetime import datetime
from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw, DNS, DNSQR


packet_count = 0


def packet_callback(packet):
    global packet_count

    # Only analyze IPv4 packets
    if IP not in packet:
        return

    packet_count += 1

    source_ip = packet[IP].src
    destination_ip = packet[IP].dst
    capture_time = datetime.now().strftime("%H:%M:%S")

    print("=" * 70)
    print(f"Packet #{packet_count}")
    print(f"Time            : {capture_time}")
    print(f"Source IP       : {source_ip}")
    print(f"Destination IP  : {destination_ip}")

    # TCP packet
    if TCP in packet:
        print("Protocol        : TCP")
        print(f"Source Port     : {packet[TCP].sport}")
        print(f"Destination Port: {packet[TCP].dport}")

    # UDP packet
    elif UDP in packet:
        print("Protocol        : UDP")
        print(f"Source Port     : {packet[UDP].sport}")
        print(f"Destination Port: {packet[UDP].dport}")

    # ICMP packet
    elif ICMP in packet:
        print("Protocol        : ICMP")

    # Other IP protocols
    else:
        print(f"Protocol Number : {packet[IP].proto}")

    # DNS information
    if DNS in packet:
        if packet[DNS].qr == 0:
            print("DNS Type        : Query")
        else:
            print("DNS Type        : Response")

        if DNSQR in packet:
            query_name = packet[DNSQR].qname.decode(errors="replace")
            print(f"DNS Query       : {query_name}")

    # Payload information
    if Raw in packet:
        payload = bytes(packet[Raw].load)
        print(f"Payload Length  : {len(payload)} bytes")
        print(f"Payload Preview : {payload[:80]!r}")
    else:
        print("Payload         : No Raw payload")

    print("=" * 70)


def main():
    print("=" * 70)
    print("              CodeAlpha Basic Network Sniffer")
    print("=" * 70)
    print("Capturing IPv4 network packets...")
    print("Press Ctrl+C to stop the sniffer.")
    print("=" * 70)
    print()

    try:
        sniff(prn=packet_callback, store=False)

    except KeyboardInterrupt:
        pass

    finally:
        print()
        print("=" * 70)
        print("Network sniffer stopped.")
        print(f"Total IPv4 packets analyzed: {packet_count}")
        print("=" * 70)


if __name__ == "__main__":
    main()