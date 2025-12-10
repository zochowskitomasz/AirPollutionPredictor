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

action=""
if [ -e $out_file ]; then
    while true; do
        echo "[$(date -Iseconds)] tools/data_retrieval/weather_data_retrieval.sh WARN: File $out_file already exists" >> $log_file
        read -p "File $out_file already exists. What do you want to do? [(O)verwrite/(A)ppend/(Q)uit] " action
        case $action in
            [Oo])
                echo "[$(date -Iseconds)] tools/data_retrieval/weather_data_retrieval.sh INFO: Overwriting $out_file..." >> $log_file
                break;;
            [Aa])
                echo "[$(date -Iseconds)] tools/data_retrieval/weather_data_retrieval.sh INFO: Appending $out_file..." >> $log_file
                break;;
            [Qq])
               echo "[$(date -Iseconds)] tools/data_retrieval/weather_data_retrieval.sh INFO: Script terminated" >> $log_file
                exit 0;;
            *)
                echo "Unrecognized input";;
        esac
    done
fi

response=$(curl -s "https://archive-api.open-meteo.com/v1/archive?latitude=52.2298&longitude=21.0118&start_date=$start_date&end_date=$end_date&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,wind_speed_10m,wind_speed_100m,surface_pressure,cloud_cover,rain,snowfall&timezone=auto")

if [ ! -z "$(echo $response | jq ".error // empty")" ]; then
    echo "[$(date -Iseconds)] tools/data_retrieval/weather_data_retrieval.sh ERROR: Data could not be retrieved from open-meteo API. Error message: $(echo $response | jq ".reason")" >> $log_file
    exit 1
else
    echo "[$(date -Iseconds)] tools/data_retrieval/weather_data_retrieval.sh INFO: Data retrieved from the API" >> $log_file
fi

{
    resp_time=$(echo $response | jq -r ".hourly.time[]")
    resp_temperature=$(echo $response | jq -r ".hourly.temperature_2m[]")
    resp_humidity=$(echo $response | jq -r ".hourly.relative_humidity_2m[]")
    resp_dew_point=$(echo $response | jq -r ".hourly.dew_point_2m[]")
    resp_app_temp=$(echo $response | jq -r ".hourly.apparent_temperature[]")
    resp_wind_10=$(echo $response | jq -r ".hourly.wind_speed_10m[]")
    resp_wind_100=$(echo $response | jq -r ".hourly.wind_speed_100m[]")
    resp_pressure=$(echo $response | jq -r ".hourly.surface_pressure[]")
    resp_cloud=$(echo $response | jq -r ".hourly.cloud_cover[]")
    resp_rain=$(echo $response | jq -r ".hourly.rain[]")
    resp_snow=$(echo $response | jq -r ".hourly.snowfall[]")
} || {
    echo "[$(date -Iseconds)] tools/data_retrieval/weather_data_retrieval.sh ERROR: There has been a problem while reading the response" >> $log_file
    exit 1
}

columns=$(echo $response | jq -r ".hourly | keys[]")
function join_by { local IFS="$1"; shift; echo "$*"; }
if [[ $action =~ [Oo] ]]; then
    echo $(join_by , $columns) > $out_file
fi

paste -d "," <(echo "$resp_time") <(echo "$resp_temperature") <(echo "$resp_humidity") <(echo "$resp_dew_point") <(echo "$resp_app_temp") <(echo "$resp_wind_10") <(echo "$resp_wind_100") <(echo "$resp_pressure") <(echo "$resp_cloud") <(echo "$resp_rain") <(echo "$resp_snow") >> $out_file

echo echo "[$(date -Iseconds)] tools/data_retrieval/weather_data_retrieval.sh INFO: script finished" >> $log_file
exit 0