#!/bin/bash

echo 'Setup garden database'
mysql /usr/garden-monitor/database/createdb.sql output.tab
mysql garden /usr/garden-monitor/database/create.sql output.tab