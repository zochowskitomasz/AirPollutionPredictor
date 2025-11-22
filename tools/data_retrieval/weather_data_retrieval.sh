#!/bin/bash
log_file="$(dirname "$0")/../../log/runtime.log"
{
    mkdir -p $(echo $log_file | grep -oP ".*/") && touch $log_file
} || {
    echo "[$(date -Iseconds)] tools/data_retrieval/weather_data_retrieval.sh ERROR: Permission denied or log file does not exist" >> $log_file
    exit 1
}

if [ "$#" -ne 3 ]; then
    echo "[$(date -Iseconds)] tools/data_retrieval/weather_data_retrieval.sh ERROR: Incorrect number of arguments passed (expected 3, got $#)" >> $log_file
    exit 1
fi

start_date=$1
end_date=$2
out_file=$3

reponse=$(curl -s "https://archive-api.open-meteo.com/v1/archive?latitude=52.2298&longitude=21.0118&start_date=$start_date&end_date=$end_date&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,wind_speed_10m,wind_speed_100m,surface_pressure,cloud_cover,rain,snowfall&timezone=auto")

if [ "$(echo $response | jq ".error")" != "null" ]; then
    echo "[$(date -Iseconds)] tools/data_retrieval/weather_data_retrieval.sh ERROR: Data could not be retrieved from open-meteo API. Error message: $(echo $response | jq ".reason")" >> $log_file
    exit 1
else
    echo "[$(date -Iseconds)] tools/data_retrieval/weather_data_retrieval.sh LOG: Data retrieved from the API" >> $log_file
fi

{
    resp_time=$(echo $response | jq ".hourly.time")
    resp_temperature=$(echo $response | jq ".hourly.temperature_2m")
    resp_humidity=$(echo $response | jq ".hourly.relative_humidity_2m")
    resp_dew_point=$(echo $response | jq ".hourly.dew_point_2m")
    resp_app_temp=$(echo $response | jq ".hourly.apparent_temperature")
    resp_wind_10=$(echo $response | jq ".hourly.wind_speed_10m")
    resp_wind_100=$(echo $response | jq ".hourly.wind_speed_100m")
    resp_pressure=$(echo $response | jq ".hourly.surface_pressure")
    resp_cloud=$(echo $response | jq ".hourly.cloud_cover")
    resp_rain=$(echo $response | jq ".hourly.rain")
    resp_snow=$(echo $response | jq ".hourly.snowfall")
} || {
    echo "[$(date -Iseconds)] tools/data_retrieval/weather_data_retrieval.sh ERROR: There has been a problem while reading the response" >> $log_file
    exit 1
}

echo "koniec"

echo $resp_time
exit 0