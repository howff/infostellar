#!/usr/bin/env python
# Test program for InfoStellar

# arb:
SATELLITE_ID = 121
GROUND_STATION_ID = 37
private_key_file = '/opr/stellarstation/etc/stellarstation-private-key.json'
certificate_file = '/opr/stellarstation/etc/tls.crt'

# Imports:
import base64
import os
import time
import grpc
import copy
from google import auth as google_auth
from google.auth import jwt as google_auth_jwt
from google.auth.transport import grpc as google_auth_transport_grpc
from stellarstation.api.v1 import stellarstation_pb2
from stellarstation.api.v1 import stellarstation_pb2_grpc

# arb added:
from google.protobuf.timestamp_pb2 import Timestamp
from pprint import pprint

# Configuration:
os.environ['GRPC_SSL_CIPHER_SUITES'] = 'ECDHE-RSA-AES128-GCM-SHA256'


# ----------------------------------------------------------------------
def run():
    # Load the private key downloaded from the StellarStation Console.
    credentials = google_auth_jwt.Credentials.from_service_account_file(
		private_key_file,
        audience='https://api.stellarstation.com')
    print("Loaded credentials")

    # Setup the gRPC client.
    jwt_creds = google_auth_jwt.OnDemandCredentials.from_signing_credentials(
        credentials)
    print("Got jwt_creds")

    # No longer required (not connecting to fakeserver)
    #channel_credential = grpc.ssl_channel_credentials(
    #    open(certificate_file, 'br').read())
    #print("Got channel_credential")

    channel = google_auth_transport_grpc.secure_authorized_channel(
        jwt_creds, None, 'api.stellarstation.com:443') # , channel_credential)
    print("Got channel")

    client = stellarstation_pb2_grpc.StellarStationServiceStub(channel)
    print("Got client")

    now = time.time() - 1000
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)
    timestamp_before = Timestamp(seconds=seconds, nanos=nanos)

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)
    timestamp_after = Timestamp(seconds=seconds, nanos=nanos)

    # Create a ListPlansRequest
    #listreq = stellarstation_pb2.ListPlansRequest()
    #listreq.satellite_id = str(SATELLITE_ID)
    # None of these work:
    #listreq.aos_before = Timestamp(timestamp_before) # TypeError: No positional arguments allowed
    #listreq.aos_before = timestamp_before # AttributeError: Assignment not allowed to field "aos_before" in protocol message object.
    #listreq.aos_before.seconds = 0 
    #listreq.aos_after.seconds = 0 
    #listreq.aos_before = timestamp_before # TypeError: Can't set composite field (when done AFTER setting seconds manually above)
    #listreq.aos_after = timestamp_after
    #listreq.aos_before = copy.deepcopy(timestamp_before) # AttributeError: Assignment not allowed to field "aos_before" in protocol message object.
    # This works:
    listreq = stellarstation_pb2.ListPlansRequest(satellite_id = str(SATELLITE_ID),
        aos_before = timestamp_before, aos_after = timestamp_after)

    print("Got listreq:")
    pprint(listreq)

    print("Sending ListPlans request:")
    client.ListPlans(listreq)
    print("Done ListPlans")


    # Open satellite stream
    #request_iterator = generate_request()
    #for value in client.OpenSatelliteStream(request_iterator):
    #    print(
    #        "Got response: ",
    #        base64.b64encode(
    #            value.receive_telemetry_response.telemetry.data)[:100])


# ----------------------------------------------------------------------
# This generator yields the requests to send on the stream opened by OpenSatelliteStream.
# The client side of the stream will be closed when this generator returns (in this example, it never returns).
def generate_request():

    # Send the first request to activate the stream. Telemetry will start
    # to be received at this point.
    yield stellarstation_pb2.SatelliteStreamRequest(satellite_id=SATELLITE_ID)

    while True:
        command_request = stellarstation_pb2.SendSatelliteCommandsRequest(
            command=[
                bytes(b'a' * 5000),
                bytes(b'b' * 5000),
                bytes(b'c' * 5000),
                bytes(b'd' * 5000),
                bytes(b'e' * 5000),
            ])

        satellite_stream_request = stellarstation_pb2.SatelliteStreamRequest(
            satellite_id=SATELLITE_ID,
            send_satellite_commands_request=command_request)

        yield satellite_stream_request
        time.sleep(3)


# ----------------------------------------------------------------------
if __name__ == '__main__':
    run()
