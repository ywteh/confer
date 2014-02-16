#!/bin/bash
pg_dump -U postgres -h confer.csail.mit.edu -p 5433 -b -F c -f "$HOME/backups/confer/confer-`date +%m-%d-%Y`.backup" confer
