#!/usr/bin/env python3
import os
import time
import math
import RNS

rns = RNS.Reticulum()

broadcast_dest = RNS.Destination(
    None,
    RNS.Destination.IN,
    RNS.Destination.PLAIN,
    "public_mesh_cam",
    "video_stream"
)

print(f"============================================================")
print(f" BROADCAST ROUTING SYSTEM ACTIVE")
print(f" Use this Channel Hash: {broadcast_dest.hash.hex()}")
print(f"============================================================")

# Reticulum broadcasts are limited to 500bytes so the frames have to be chunked

try:
    while True:
        if os.path.exists("/tmp/livecam.txt"):
            with open("/tmp/livecam.txt", "r") as f:
                frame_data = f.read()
            
            raw_bytes = frame_data.encode('utf-8', errors='ignore')
            
            chunk_size = 400
            total_chunks = math.ceil(len(raw_bytes) / chunk_size)
            
            for i in range(total_chunks):
                start = i * chunk_size
                end = start + chunk_size
                chunk_payload = raw_bytes[start:end]
                
                header = bytes([i, total_chunks])
                packet_data = header + chunk_payload
                
                packet = RNS.Packet(broadcast_dest, packet_data)
                packet.send()
                time.sleep(0.01) # Ultra-short delay to prevent network interface congestion
            
        # This is for 2 frames per second
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nBroadcast stream deactivated.")
