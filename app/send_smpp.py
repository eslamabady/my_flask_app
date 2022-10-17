from app import app
from flask import request,jsonify,make_response
import smpplib

@app.route('/post/<username>/<password>/<service_ip>:<port>',methods=['POST','GET'])
def send(username,password,service_ip,port):
    req_rec=request.get_json()
    client = None
    try:
        client = smpplib.client.Client(service_ip,port)
        client.connect()
        try:
            client.bind_transmitter(system_id=username, password=password)
            print("ccccc")

            for req in req_rec:
                client.send_message(source_addr_ton=smpplib.consts.SMPP_TON_INTL,
                                    source_addr=req['source_number'],
                                    dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
                                    destination_addr=req['dst_number'],
                                    short_message=req['content'])
            return make_response(jsonify({'message': 'Sucess'}), 200)
        finally:
            # print "==client.state====", client.state
            if client.state in [smpplib.consts.SMPP_CLIENT_STATE_BOUND_TX]:
                # if bound to transmitter
                try:
                    client.unbind()
                except smpplib.exceptions.UnknownCommandError as ex:
                    # https://github.com/podshumok/python-smpplib/issues/2
                    try:
                        client.unbind()
                    except smpplib.exceptions.PDUError as ex:
                        pass
    finally:

        if client:
            # print "==client.state====", client.state
            client.disconnect()
            # print "==client.state====", client.state
        return make_response(jsonify({'message': 'Sucess'}), 200)