import sys
import json

def mapper():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            vessel = data.get('Vessel', 'Unknown')
            rig = data.get('Rig', 'Unknown')
            departure = data.get('ApproximateDeparture', 'Unknown')
            rank = data.get('Rank')
            
            # Key: Vessel and Rig
            # Value: (departure, is_crew, is_passenger)
            is_crew = 1 if rank else 0
            is_passenger = 0 if rank else 1
            
            # Emit key and values separated by tab
            # We include departure in the value to count unique trips in the reducer
            # Format: vessel|rig \t departure|is_crew|is_passenger
            print(f"{vessel}|{rig}\t{departure}|{is_crew}|{is_passenger}")
        except json.JSONDecodeError:
            continue

if __name__ == "__main__":
    mapper()
