import sys

def reducer():
    current_key = None
    sum_crew = 0
    sum_passenger = 0
    trips = set()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        try:
            key, value = line.split('\t')
            departure, is_crew, is_passenger = value.split('|')
            is_crew = int(is_crew)
            is_passenger = int(is_passenger)
            
            if current_key == key:
                sum_crew += is_crew
                sum_passenger += is_passenger
                trips.add(departure)
            else:
                if current_key:
                    # Output: vessel, rig, num_trips, passengers, crew
                    vessel, rig = current_key.split('|')
                    print(f"{vessel}\t{rig}\t{len(trips)}\t{sum_passenger}\t{sum_crew}")
                
                current_key = key
                sum_crew = is_crew
                sum_passenger = is_passenger
                trips = {departure}
        except ValueError:
            continue

    # Output the last key
    if current_key:
        vessel, rig = current_key.split('|')
        print(f"{vessel}\t{rig}\t{len(trips)}\t{sum_passenger}\t{sum_crew}")

if __name__ == "__main__":
    reducer()
