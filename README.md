# simple-detection-platform
Simple Detection Platform is a platform that provides a simple web interface for deploying, managing, and testing security detections. The platform supports delivering detections in either Sigma or tool-native format to multiple different security platforms (Splunk, SentinelOne, CrowdStrike Falcon) but also supports custom outputs defined in YAML. 


## Table of Contents
- [Architecture](#architecture)
- [Considerations](#considerations)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)

## Development Resources
- https://stackoverflow.com/questions/45128902/psycopg2-and-sql-injection-security
- https://stackoverflow.com/questions/19098551/psycopg2-not-returning-results
- https://stackoverflow.com/questions/62838826/inserting-data-to-a-postgresql-table-through-streamlit
- https://docs.streamlit.io/develop/tutorials/databases/postgresql
- https://stackoverflow.com/questions/41637505/how-to-persist-data-in-a-dockerized-postgres-database-using-volumes
- https://www.youtube.com/watch?v=G-5c25DYnfI
- https://stackoverflow.com/questions/7718585/how-to-set-auto-increment-primary-key-in-postgresql
- https://stackoverflow.com/questions/26598738/how-to-create-user-database-in-script-for-docker-postgres
- https://stackoverflow.com/questions/435424/postgresql-how-to-create-table-only-if-it-does-not-already-exist

## Next Steps
- Test if dockerize postgres database is persist
- Create mysql script that creates initial detection table
- Use DB as a "cache" for remembering tool selection?
    - entry that updates as the user selects or removes tools.
    - tool_selection_table where there's a column labeled selection that contains what they selected on the overview page.
    - if they select a new tool, the entry is updated to reflect the new tool.
    - if they remove a tool, the entry is also updated


## Architecture

## Requirements

## Installation

## Configuration

## Usage

