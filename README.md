# infostellar
Use the InfoStellar API to schedule antenna time availability

See https://github.com/infostellarinc/stellarstation-api

See https://github.com/infostellarinc/stellarcli/releases

# Installation
```
virtualenv -p /usr/bin/python3 /opr/stellarstation
source /opr/stellarstation/bin/activate
pip install --upgrade stellarstation
```

Download api key from https://www.stellarstation.com/console
and place into the etc directory, named `etc/stellarstation-private-key.json`

# Usage
```
source /opr/stellarstation/bin/activate
bin/test.py
```

# Command line
```
mkdir -p $HOME/.config/stellar/
cp $doc/station/projects/InfoStellar/stellarstation-private-key.json $HOME/.config/stellar/stellarstation_credentials.json
```
Then run
```
$doc/station/projects/InfoStellar/stellar ground-station list-plans 37
```

# Notes
The basic concept of operation is:
the ground station owner tells StellarStation when their ground station is not available using the  'AddUnavailabilityWindow' Call.  
StellarStation treats all other time as available, and schedules passes for satellite operators.
You can see the passes that are currently scheduled at your ground station using the 'ListPlans' Call. 

Fake ground station ID = 37
Fake satellite ID = 121 (NORAD 99995)
https://www.stellarstation.com/console/antenna/37

```
  rpc ListPlans (ListPlansRequest) returns (ListPlansResponse);
  ListPlansRequest is
  string satellite_id = 1;
  google.protobuf.Timestamp aos_after = 2;
  google.protobuf.Timestamp aos_before = 3;
```

A timestamp object: See https://developers.google.com/protocol-buffers/docs/pythontutorial
```
now = time.time()
seconds = int(now)
nanos = int((now - seconds) * 10**9)
timestamp = Timestamp(seconds=seconds, nanos=nanos)
```
