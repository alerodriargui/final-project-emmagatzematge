# Analysis of 19th-Century Maritime Voyages in the Americas: A MapReduce Study

**Course**: Emmagatzematge (Storage)  
**Project**: Final Project - Option B (MapReduce)  
**Author**: [USER NAME]  
**Date**: January 2026

---

## 1. Introduction and Historical Context

During the 19th century, the Americas experienced a golden age of maritime activity. This era was characterized by two major phenomena: the peak of the American whaling industry and a massive wave of migration from Europe and other parts of the world.

The United States, particularly New England ports like New Bedford and Nantucket, became the global epicenter of whaling. Whaling ships, often rigs like Barks and Ships, would embark on multi-year voyages to the Pacific, Arctic, and Indian Oceans. These voyages were not just economic ventures but also complex social environments, carrying diverse crews of experienced sailors, harpooners, and "greenhands" from various origins.

Simultaneously, passenger sailing ships were the primary means of transoceanic migration. After 1820, the U.S. government began requiring passenger manifests, providing a rich demographic record of the millions who sought new lives in the Americas.

This project utilizes a database (converted to JSON format in `CrewJSON.json`) containing records of passengers and crew members from this period. The objective is to apply MapReduce techniques to distill this large dataset into meaningful insights about the vessels, their rigs, and the composition of their travelers and staff.

## 2. Methodology: MapReduce

### 2.1 Overview of MapReduce
MapReduce is a programming model and an associated implementation for processing and generating large datasets. It is designed to scale across thousands of machines in a cluster, but its core principles remain highly effective for structured data analysis on single machines as well.

The model consists of two primary functions:
- **Map**: Processes input data and produces a set of intermediate key-value pairs.
- **Reduce**: Merges all intermediate values associated with the same intermediate key.

### 2.2 Application to the Vessel Study
For this project, the **Vessel Study** was selected. The goal was to analyze voyages by vessel and rig, identifying the number of trips, total passengers, and total crew members.

#### The Mapper Logic
The mapper reads the `CrewJSON.json` file line by line. For each record:
1. It extracts the `Vessel` and `Rig` fields.
2. It identifies the `ApproximateDeparture` to help distinguish unique voyages.
3. It determines if the individual is a crew member (has a `Rank` specified) or a passenger (no `Rank`).
4. It emits a key-value pair:
   - **Key**: `Vessel|Rig`
   - **Value**: `Departure|is_crew|is_passenger`

#### The Reducer Logic
The reducer receives the sorted output from the mapper. Since all records for a specific Vessel/Rig combination are grouped together, the reducer can:
1. Count the unique departure dates to estimate the number of documented "trips" or segments.
2. Sum the crew members and passengers.
3. Emit the final aggregated record: `Vessel`, `Rig`, `Number of Trips`, `Total Passengers`, `Total Crew`.

This process effectively transforms a list of 168,366 individual records into a consolidated OLAP (Online Analytical Processing) cube of 1,368 unique vessel-rig combinations.

## 3. Work Carried Out

The project was executed in the following stages:

1.  **Data Inspection**: Initial exploration of `CrewJSON.json` revealed 168,366 lines of data. Sparsity analysis showed that while physical characteristics (like eye color) were rare, voyage-related data (Vessel, Rig, Rank) was robust.
2.  **Code Implementation**:
    - `mapper.py`: A Python script to extract relevant fields and emit intermediate keys.
    - `reducer.py`: A Python script to perform aggregations and unique trip counts.
3.  **Data Processing**: The MapReduce pipeline was executed using a standard Unix-style pipe:
    ```bash
    cat CrewJSON.json | python mapper.py | sort | python reducer.py > results.tsv
    ```
4.  **Data Visualization**: Using the `pandas` and `matplotlib` libraries, several charts were generated to interpret the findings.
5.  **OLAP Cube Generation**: The final output provides a structured view of the maritime data, ready for multidimensional analysis.

## 4. Database Structure

The project handles data in three primary states:

### 4.1 Input Format (JSON)
Each record in `CrewJSON.json` follows this schema:
- `LastName`, `FirstName`: Names of the person.
- `Vessel`: String identifier of the ship.
- `Rig`: Type of vessel (e.g., Bark, Ship, Schr, Brig).
- `ApproximateDeparture`: Date string.
- `Rank`: Occupational role (if absent, the person is a passenger).
- `Residence`, `Skin`, `Hair`, `Height`: Optional personal characteristics.

### 4.2 Intermediate Format (Key-Value)
- **Key**: `Vessel_Name|Rig_Type`
- **Value**: `Date|1/0|0/1`

### 4.3 Output Format (OLAP Cube / TSV)
The resulting cube contains:
1.  **Vessel**: The ship's name.
2.  **Rig**: The ship's rig type.
3.  **NumTrips**: Count of unique departure dates recorded.
4.  **TotalPassengers**: Sum of records without a rank.
5.  **TotalCrew**: Sum of records with a rank.

## 5. Results and Analysis

The analysis produced a dataset of over 1,300 vessel-rig segments. Below are the key findings.

### 5.1 Top Vessels by Volume
The chart "Top 10 Vessels by Total Passengers and Crew" shows the most active ships in the database. 
[PLACEHOLDER: top_10_vessels.png]

Large ships like the *Canton II*, *Alice Knowles*, and *Commodore Perry* appear prominently. Many of these names are synonymous with the New Bedford whaling fleet, suggesting the dataset's heavy lean towards whaling activity.

### 5.2 Population Distribution by Rig
The "Passengers vs Crew by Rig Type" chart highlights how different vessel types were utilized.
[PLACEHOLDER: rig_distribution.png]

- **Ships and Barks**: These were the primary rigs for long-distance voyages. They show a high volume of both passengers and crew.
- **Schooners (Schr) and Brigs**: These smaller rigs were often used for coastal trade or shorter whaling stints, typically carrying smaller groups.

### 5.3 Average Occupancy per Trip
The "Average People per Trip by Rig Type" chart reveals the carrying capacity or documentation density of different rigs.
[PLACEHOLDER: avg_per_trip_rig.png]

Surprisingly, certain rigs like "Ships" and "Barks" maintain higher averages, reflecting their role as the "jumbos" of the 19th-century maritime world.

## 6. Conclusions

The MapReduce study of the 19th-century maritime database has successfully demonstrated the power of distributed processing techniques even on a local scale. 

Key takeaways include:
- **Efficiency**: Processing 168k records took only seconds using the MapReduce paradigm, proving its scalability for much larger datasets.
- **Data Insights**: We identified that while many vessels carried small crews, a significant portion of the maritime population consisted of passengers, particularly on larger "Ship" and "Bark" rigs.
- **Data Quality**: The study highlighted variations in rig naming (e.g., "Schooner" vs "Schr"), indicating a need for data normalization in future studies.

This project provides a foundational OLAP cube that can be further extended to include year-over-year trends or residency analysis (migratory patterns), offering a window into the maritime laborers and travelers who shaped the Americas in the 1800s.

---
## Appendix: Source Code

### Mapper (`src/mapper.py`)
```python
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
            print(f"{vessel}|{rig}\t{departure}|{is_crew}|{is_passenger}")
        except json.JSONDecodeError:
            continue

if __name__ == "__main__":
    mapper()
```

### Reducer (`src/reducer.py`)
```python
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
                    vessel, rig = current_key.split('|')
                    print(f"{vessel}\t{rig}\t{len(trips)}\t{sum_passenger}\t{sum_crew}")
                
                current_key = key
                sum_crew = is_crew
                sum_passenger = is_passenger
                trips = {departure}
        except ValueError:
            continue

    if current_key:
        vessel, rig = current_key.split('|')
        print(f"{vessel}\t{rig}\t{len(trips)}\t{sum_passenger}\t{sum_crew}")

if __name__ == "__main__":
    reducer()
```
