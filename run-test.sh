#!/bin/bash
############################################################################
# This script is used to start exabgp instances with predefined test configs
# supported tests are ROUTE-001, ROUTE-002, and ROUTE-003
############################################################################
# set working directory to location of script
cd "${0%/*}"

# use getopts to parse parameters
while getopts ":t:hn:s" opt; do
  case $opt in
    h)
      echo "Usage: run-test.sh [-t testname -n peercount]"
      echo "       run-test.sh [-s]"
      echo "Options:"
      echo "   -t    testname, e.g. ROUTE-001"
      echo "   -n    number of exabgp instances, optional, default is 1"
      echo "   -s    stop all instances"
      echo "   -h    show this message"
      exit 0
      ;;
    n)
      peercount="$OPTARG"
      ;;
    s)
      stop=true
      ;;
    t)
      testname="$OPTARG"
      ;;
    \?)
      echo "Invalid option -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires argument." >&2
      exit 1
      ;;
  esac
done

# if -s is called, stop all instances and exit
if [ $stop ]; then
  echo "Stopping all processes.."
  pids=`screen -ls | grep "peer-*" | cut -d . -f 1 | awk '{print $1}'`
  count=0
  for i in $pids; do
    kill $(ps h --ppid $i -o pid)
    ((count++))
  done
echo "Killed $count processes."
exit 0
fi

# if -n is not present, set peercount to 1
if [ -z "$peercount" ]; then
  peercount=1
fi

# if -t is not present, throw error and exit
if [ -z "$testname" ]; then
  echo "No test name provided. See run-test.sh -h for help."
  exit 1
fi

# build log file path
timestamp=$(date +"%Y%m%d_%H%M%S")
logpath="logs/$testname/$timestamp"
mkdir $logpath

# this script tracks running instances by setting the screen session name to peer-<id>
# check if instances are already running, use first free id to start new instance
echo "Starting $peercount instances for test $testname.."
count=0
peerid=1
while [ $peercount -gt 0 ]; do
  if [[ $(screen -ls | grep "peer-$peerid") ]]; then
    ((peerid++))
  else
    screen -L -Logfile "$logpath/peer-$peerid.log" -S peer-$peerid -d -m ../exabgp/sbin/exabgp -d configs/exabgp/$testname/peer-$peerid.conf
    ((peercount--))
    ((count++))
    ((peerid++))
  fi
done
echo "Started $count instances."
