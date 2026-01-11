#!/bin/bash
log_file="$(dirname "$0")/../../log/runtime.log"
{
    mkdir -p $(echo $log_file | grep -oP ".*/") && touch $log_file
} || {
    echo "[$(date -Iseconds)] tools/data_retrieval/pollution_data_retrieval.sh ERROR: Permission denied or log file does not exist" >> $log_file
    exit 1
}

if [ "$#" -ne 3 ]; then
    echo "[$(date -Iseconds)] tools/data_retrieval/pollution_data_retrieval.sh ERROR: Incorrect number of arguments passed (expected 3, got $#)" >> $log_file
    exit 1
fi

start_date=$1
end_date=$2
out_file=$3

sensor_ids=(3575 3576 3579 3580 3581 3584 3585)
sensor_names=("c6h6" "co" "no" "no2" "nox" "pm10" "pm25")

for i in ${!sensor_ids[@]}; do
    response=$(curl -s "https://api.gios.gov.pl/pjp-api/v1/rest/archivalData/getDataBySensor/${sensor_ids[$i]}?dateFrom=$start_date%2000%3A00&dateTo=$end_date%2023%3A00&size=500")

    if [ ! -z "$(echo $response | jq ".error_result // empty")" ]; then
        echo "[$(date -Iseconds)] tools/data_retrieval/pollution_data_retrieval.sh ERROR: Data could not be retrieved from GIOŚ PJP API. Error message: $(echo $response | jq ".error_reason")" >> $log_file
        exit 1
    else
        if [ $i -eq 0 ]; then 
            dates=( $(echo $response | jq '."Lista archiwalnych wyników pomiarów"[]."Data"') )
        fi
        tmp_values=( $(echo $response | jq '."Lista archiwalnych wyników pomiarów"[]."Wartość"') )
        echo "[$(date -Iseconds)] tools/data_retrieval/pollution_data_retrieval.sh INFO: Data retrieved from the API" >> $log_file
    fi

    total_pages=$(echo $response | jq ".totalPages")

    for ((p = 1 ; p < $total_pages ; p++)); do
        response=$(curl -s "https://api.gios.gov.pl/pjp-api/v1/rest/archivalData/getDataBySensor/${sensor_ids[$i]}?dateFrom=$start_date%2000%3A00&dateTo=$end_date%2000%3A00&size=500&page=$p")

        if [ $i -eq 0 ]; then
            dates+=( $(echo $response | jq '."Lista archiwalnych wyników pomiarów"[]."Data"') )
        fi
        tmp_values+=( $(echo $response | jq '."Lista archiwalnych wyników pomiarów"[]."Wartość"') )
    done

    if [ $i -eq 0 ]; then
        dates_nospace=$(echo ${dates[@]} | sed "s/\:00\"\s/\n/g" | sed "s/\s/T/g" | sed "s/\"//g")
    fi
    
    declare "${sensor_names[$i]}_values"="$(printf "%s\n" "${tmp_values[@]}")"
done

function join_by { local IFS="$1"; shift; echo "$*"; }
echo -n "time," > $out_file
echo $(join_by , ${sensor_names[@]}) >> $out_file

paste -d "," <(echo "$dates_nospace") <(echo "$c6h6_values") <(echo "$co_values") <(echo "$no_values") <(echo "$no2_values") <(echo "$nox_values") <(echo "$pm10_values") <(echo "$pm25_values") >> $out_file

chmod 666 $out_file

echo echo "[$(date -Iseconds)] tools/data_retrieval/pollution_data_retrieval.sh INFO: script finished" >> $log_file
exit 0
