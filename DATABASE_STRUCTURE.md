# Database Structure

The project processes historical maritime data from a JSON source and produces an aggregated analytical dataset (OLAP Cube).

## 1. Input Data Structure (CrewJSON.json)

The input is a JSONL (JSON Lines) file where each line is a JSON object representing one person (passenger or crew member).

### Fields:
- **LastName**: (String) Passenger or crew member's last name.
- **FirstName**: (String) First name(s) and initials.
- **Vessel**: (String) Name of the sailing vessel.
- **Rig**: (String) Type of vessel (e.g., Ship, Bark, Brig, Schooner, etc.).
- **ApproximateDeparture**: (String) Date of departure in various formats (e.g., "MM/DD/YYYY" or "YYYY-Month").
- **Rank**: (String, Optional) The professional position of a crew member (e.g., "1st Mate", "Seaman"). If this field is missing, the person is classified as a **Passenger**.
- **Height**: (String, Optional) Physical height (e.g., "5ft 6in").
- **Age**: (String, Optional) Age of the person.
- **Skin**: (String, Optional) Skin color description.
- **Hair**: (String, Optional) Hair color/type description.
- **Eye**: (String, Optional) Eye color description.
- **Residence**: (String, Optional) Place of origin or residence.

## 2. Processed Data / OLAP Cube Structure (output/vessel_study_results.tsv)

The MapReduce output is a Tab-Separated Values (TSV) file representing an OLAP cube indexed by Vessel and Rig.

### Columns:
1. **Vessel**: (Dimension) Ship name.
2. **Rig**: (Dimension) Vessel type.
3. **Number of Trips**: (Measure) Total unique departure dates found for this vessel-rig combination.
4. **Total Passengers**: (Measure) Total number of individuals without a `Rank` associated with this vessel.
5. **Total Crew**: (Measure) Total number of individuals with a `Rank` associated with this vessel.

## 3. Relationships and Constraints
- Each record originates from a specific voyage identified by `(Vessel, Rig, ApproximateDeparture)`.
- The distinction between Passenger and Crew is binary based on the presence of the `Rank` attribute.
- All physical characteristics (Height, Age, etc.) are associated with individual records but were not aggregated in the Vessel Study.
