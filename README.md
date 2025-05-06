# Drone Imagery Search System - User Guide

## Purpose

We worked with a stakeholder, Kala’i Ellis, a Spatial Data Analyst at the Spatial Analysis Laboratory (SAL) at Smith College for this project. For the project, we set out to produce a system that could organize many files and that was relatively easy to keep updated. Drone use has been rising in projects at Smith. Each month, 10-20 separate drone flights occur, with each having individual folders with images and metadata that are stored by month and specific date. Some files can be shared and utilized across multiple projects. The files from these drone flights are currently being stored in Google Drive. However, it was difficult to recall past data, and it was very time-intensive to find information for new projects from existing folders. We created a searchable database that is linked to the Google Drive data from the SAL and can be updated monthly. Using our database and an accompanying front-end tool, you can filter projects by date and type, making this database easier to parse through and more accessible for members other than Kala’i in the lab. 

Link to our [presentation](https://docs.google.com/presentation/d/11lS9HENt4-R_IivPTkeSB0FKPf23oE93byotoBUc3-o/edit?usp=sharing) where we ran through the key aspects of our project (accessible to anyone at Smith College). 

## Included Files
- `drones_final_search_bydate_and_map.ipynb`: Main application with database setup, data import, and Flask web interface
- [Folder] `old files`: Includes deprecated files from our old, local setup, which uses Postgres.


## How to Use
1. **Access the System**: Open the notebook in Colab and run all cells
2. **Search Interface**:
   - Select date range (From/To)
   - Choose imagery type (All, Professional, or Personal)
   - Click "Search"



https://github.com/user-attachments/assets/b91f6bcb-5076-4ae7-bc66-edf3ad3a8d67




## Setup Instructions
1. Open `drone_search_system.ipynb` in Google Colab
2. Replace source path to dataset Google Drive path (i.e `folder_path = '/content/drive/Shareddrives/Drones - CSC 230/10-October'`)
3. Run all cells sequentially
4. The web interface will automatically launch in the notebook; Choose between Search by date/type and map interface
5. For direct access, click the generated URL

   



https://github.com/user-attachments/assets/3f9bc45e-0d29-4e80-93fc-1328579b3f34







## Dependencies
- Python 3
- Flask
- pandas
- sqlite3
- Google Colab environment

## Features
- **Date Filtering**: Find all flights between specific dates
- **Project Type**: Filter by professional or personal projects
- **Direct Links**: Access original files in Google Drive

## Tips
- Professional files follow `"DJI_YYYYMMDDHHMM"` format
- Personal files use `"MM.DDDescription"` format
- The system automatically detects and classifies both types

