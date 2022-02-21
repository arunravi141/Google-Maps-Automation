#!/bin/bash

FAIL=0
TOKEN=7bb42a99111c486aa79677de182498b0
t=0
echo "Starting test execution"

testName="search_place_test"
START=1
END=5

for i in {$START..$END} ; do
  printf "Executing the test: [%s.py]" "$testName"
  pytest scripts/"$testName.py" --udid ZY3236NZWT --appium_input https://dev-us-nyc-0.headspin.io:7008/v0/7bb42a99111c486aa79677de182498b0/wd/hub --os android --network_type WIFI -v -s &
  t=$((t+1))
#   pytest scripts/"$testName.py" --udid 223303d01c027ece --appium_input https://ae-dxb.headspin.io:7000/v0/7bb42a99111c486aa79677de182498b0/wd/hub --os android --network_type WIFI -v -s &
#   t=$((t+1))
  pytest scripts/"$testName.py" --udid 00008030-001C64280CA0802E --appium_input https://gb-lhr.headspin.io:7200/v0/7bb42a99111c486aa79677de182498b0/wd/hub --os ios --network_type WIFI -v -s &
  t=$((t+1))
  pytest scripts/"$testName.py" --udid c632061d251cdaa9bea50781980ce3b0ff219709 --appium_input https://dev-us-pao-1.headspin.io:7010/v0/7bb42a99111c486aa79677de182498b0/wd/hub --os ios --network_type WIFI -v -s &
  t=$((t+1))
done

echo "Test PID's: $(jobs -p)"

for job in $(jobs -p); do
  wait $job || let "FAIL+=1"
done

if [ "$FAIL" == "0" ]; then
  echo "All" $t "test executed successfully"
else
  echo "($FAIL/$t) tests failed. Please see Ford Dashboard for details"
  exit 1
fi
