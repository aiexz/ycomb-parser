# HN Comments Parser
## How it works?
Every 10 seconds we make a request to HN `/newcomments` page to parse comments and save to database. 

API just provides last rows from database
## What works:
- Comment parser
- Last X comments
- Comments by user
- Migrations
- [Optional] sentiment analysis of comment text
## Untested
- Docker image
## Works partially
- Tests(I believe it is due to sqlite although I use aiosqlite)
