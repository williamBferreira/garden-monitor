#!/bin/bash

echo 'Setup garden database'
mysql garden /usr/garden-monitor/database/create.sql output.tab