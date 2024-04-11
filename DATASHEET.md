# Motivation
1. For what purpose was the dataset created? Was there a specific task in mind? Was there a
specific gap that needed to be filled?

This data is distributed to the public in the form of PDF files. This information is provided for public awareness. The dataset is created to build a pipeline on the information provided to extract valuable information and augment additional insights from the original information.

2. Who created the dataset (e.g., which team, research group) and on behalf of which entity
(e.g., company, institution, organization)?

The Norman, Oklahoma police department regularly reports incidents, arrests, and other activities. This data is hosted on their website. 

3. Who funded the creation of the dataset?

The creation of the dataset is funded and managed by Norman police department in Oklahoma.

4. Any other comments?

No

# Composition
1. What do the instances that comprise the dataset represent (e.g., documents, photos, people,
countries)? 

The instances that comprise the dataset represent the incidents happening in the Norman city of Oklahoma.

2. How many instances are there in total (of each type, if appropriate)?

There are 5 instances of type string.

3. Does the dataset contain all possible instances or is it a sample (not necessarily random) of
instances from a larger set? 

The dataset itself contains all possible instances.

4. What data does each instance consist of? 

Each instance consists of a date and time, address, nature and ori number of the incident.

5. Is there a label or target associated with each instance?

There is no target associated with each instance

6. Is any information missing from individual instances?

Few instances do not contain name of the city and state. Few instances don't have any address at all.

7. Are relationships between individual instances made explicit?

No, the dataset does not explicitly define relationships between individual instances. Each entry represents a discrete incident or activity without explicit connections to other entries.

8. Are there recommended data splits?

Yes, recommended data splits might include separating the dataset into training, validation, and testing subsets to facilitate model development and evaluation. For instance, a common split could be 70% training, 15% validation, and 15% testing.

9. Are there any errors, sources of noise, or redundancies in the dataset?

Errors, noise, and redundancies could exist in the dataset due to various factors such as human error in data entry, inconsistent formatting, or duplication of records.

10. Is the dataset self-contained or reliant on external resources?

The dataset appears to be self-contained, as it is presented in a CSV format without explicit references to external resources.

11. Does the dataset contain confidential data?

The dataset does not appear to contain confidential data as it primarily consists of incident reports and activities conducted by public authorities.

12. Does the dataset contain potentially offensive content?

The dataset contains records of police incidents, which might include descriptions of sensitive or distressing events. However, the dataset itself does not contain offensive content.

13. Does the dataset relate to people?

Yes, the dataset relates to people indirectly through incident reports and activities involving individuals.

14. Is it possible to identify individuals from the dataset?

Direct identification of individuals from the dataset is unlikely as it primarily contains anonymized incident reports. However, indirect identification could be possible in some cases.

15. Does the dataset contain sensitive data?

The dataset may contain data related to individuals' interactions with law enforcement, which could be considered sensitive depending on the nature of the incidents.

16. Any other comments?

The dataset provides valuable insights into police activities and incident reports but may require further preprocessing and analysis for specific research or application purposes.

