import argparse
import csv
from assignment0.main import main
from collections import Counter

def augment_location_ranks(all_incidents):
    # Extract locations from the tuples in the incidents_list
    locations = [incident[4] for incident in all_incidents]
    # Count the frequency of each location
    location_counts = Counter(locations)

    # Assign ranks to locations based on their frequency
    sorted_locations = sorted(location_counts.items(), key=lambda x: (-x[1], x[0]))

    # Assign ranks cumulatively
    cumulative_rank = 1
    location_ranks = {}
    for location, count in sorted_locations:
        location_ranks[location] = cumulative_rank
        cumulative_rank += count

    # Update the tuples in the incidents_list with the corresponding location ranks
    updated_incidents_list = [(incident[0], incident[1], incident[2], incident[3], incident[4], incident[5], incident[6], incident[7], incident[8], location_ranks.get(incident[4], 1000)) for incident in all_incidents]
    return updated_incidents_list

def augment_incident_ranks(all_incidents):
    # Extract incidents from the tuples in the incidents_list
    incidents = [incident[6] for incident in all_incidents]
    # Count the frequency of each location
    incident_counts = Counter(incidents)
    # Assign ranks to locations based on their frequency
    sorted_incidents = sorted(incident_counts.items(), key=lambda x: (-x[1], x[0]))
    # Assign ranks cumulatively
    cumulative_rank = 1
    incident_ranks = {}
    for incident, count in sorted_incidents:
        incident_ranks[incident] = cumulative_rank
        cumulative_rank += count
    
    # Update the tuples in the incidents_list with the corresponding location ranks
    updated_incidents_list = [(incident[0], incident[1], incident[2], incident[3], incident[4], incident[5], incident[6], incident[7], incident[8], incident[9], incident_ranks.get(incident[6], 1000)) for incident in all_incidents]
    return updated_incidents_list

def augment_emsstat(all_incidents):
    for i, incident in enumerate(all_incidents):
        bool_value = False
        current_ori = incident[7]
        if current_ori == 'EMSSTAT':
            bool_value = True
        else:
            next_incidents = all_incidents[i+1:i+3]
            bool_value = any(next_inc[7] == 'EMSSTAT' and next_inc[2] == incident[2] and next_inc[4] == incident[4] for next_inc in next_incidents)
        all_incidents[i] = (incident[0], incident[1], incident[2], incident[3], incident[4], incident[5], incident[6], incident[7], incident[8], incident[9], incident[10], bool_value)
    return all_incidents

def process_urls(urls_file):
    with open(urls_file, 'r') as file:
        urls = csv.reader(file)
        for url in urls:
            all_incidents = main(url[0])
            all_incidents = augment_location_ranks(all_incidents)
            all_incidents = augment_incident_ranks(all_incidents)
            all_incidents = augment_emsstat(all_incidents)
            for incident in all_incidents:
                row = "\t".join(map(str, [incident[0], incident[1], incident[6], incident[9], incident[5], incident[10], incident[7], incident[11]]))
                print(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", required=True, help="Path to the CSV file containing a list of URLs")
    args = parser.parse_args()

    process_urls(args.urls)

# if __name__ == "__main__":
#     all_incidents = main("https://www.normanok.gov/sites/default/files/documents/2024-03/2024-03-04_daily_incident_summary.pdf")
#     all_incidents = augment_location_ranks(all_incidents)
#     all_incidents = augment_incident_ranks(all_incidents)
#     all_incidents = augment_emsstat(all_incidents)
#     print(all_incidents[0])