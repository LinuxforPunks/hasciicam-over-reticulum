#!/usr/bin/env python3
import sys
import time
import RNS

if len(sys.argv) < 2:
    print("Usage: python3 watch_stream.py [channel_hash]")
    sys.exit(1)

channel_hash_hex = sys.argv[1]
RNS.Reticulum()

try:
    channel_bytes = bytes.fromhex(channel_hash_hex)
except ValueError:
    print("Error: Invalid hexadecimal channel hash.")
    sys.exit(1)

listen_dest = RNS.Destination(
    None,
    RNS.Destination.IN,
    RNS.Destination.PLAIN,
    "public_mesh_cam",
    "video_stream"
)
listen_dest.direction = RNS.Destination.OUT
listen_dest.hash = channel_bytes

received_chunks = {}

def on_packet_received(data, packet):
    global received_chunks
    if data and len(data) > 2:
        try:
            chunk_idx = data[0]
            total_chunks = data[1]
            chunk_payload = data[2:]
            
            received_chunks[chunk_idx] = chunk_payload
            
            if len(received_chunks) == total_chunks:
                full_frame_bytes = b""
                for idx in range(total_chunks):
                    full_frame_bytes += received_chunks[idx]
                
                raw_text = full_frame_bytes.decode('utf-8', errors='ignore')
                clean_text = raw_text.replace("```", "").replace("# Live HasciiCam Feed", "")
                
                sys.stdout.write("\033[H\033[J")
                sys.stdout.write(clean_text.strip() + "\n")
                sys.stdout.flush()
                
                received_chunks.clear()
        except Exception:
            pass

listen_dest.set_packet_callback(on_packet_received)

print("Tuned into Reticulum Live Video Stream... Reassembling frames.")
print("Press [Ctrl + C] to disconnect.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nTuned out of stream.")
