#!/bin/bash

BASE_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
TOKEN= #put api token here
CITY="warszawa"

JSON=$(curl -s "https://api.waqi.info/feed/$CITY/?token=$TOKEN" | sed -n '/^{/,$p')

TIME=$(echo "$JSON" | jq -r '.data.time.s')

PM25=$(echo "$JSON" | jq '.data.iaqi.pm25.v')

TEMP=$(echo "$JSON" | jq '.data.iaqi.t.v')

PRESS=$(echo "$JSON" | jq '.data.iaqi.p.v')

HUM=$(echo "$JSON" | jq '.data.iaqi.h.v')

WIND=$(echo "$JSON" | jq '.data.iaqi.w.v')

NOW=$(date '+%Y-%m-%d %H:%M:%S')

LOG_FILE="$BASE_DIR/marszalkowska_log.csv"
ERROR_LOG="$BASE_DIR/marszalkowska_error.log"

echo "$NOW;$TIME;$PM25;$TEMP;$PRESS;$HUM;$WIND" >> "$LOG_FILE" 2>> "$ERROR_LOG"
