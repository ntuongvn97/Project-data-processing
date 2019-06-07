from flask import Flask, render_template
from flask_mqtt import Mqtt
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from ast import literal_eval
import logging

app = Flask(__name__)
# use the free broker from HIVEMQ
app.config['MQTT_BROKER_URL'] = 'mqtt'
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
# set the username here if you need authentication for the broker
app.config['MQTT_USERNAME'] = ''
# set the password here if the broker demands authentication
app.config['MQTT_PASSWORD'] = ''
# set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_KEEPALIVE'] = 5
# set TLS to disabled for testing purposes
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)
data_received = {}


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('topic/data')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global data_received
    data_received = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data_received)


def handle_show_data(data):
    fig = figure(plot_width=600, plot_height=300)
    fig.vbar(
        x=list(data.keys()),
        width=0.5,
        bottom=0,
        top=list(data.values()),
        color='navy'
    )

    # script, div
    return components(fig)


def handle_data_recieved(data_received):
    data_return = []
    logging.warn("data reurn %r", data_return)
    data = literal_eval(data_received['payload'])

    if data.get("ticket"):
        for key in data['ticket']:
            if key == "_type":
                data['ticket'][key][0] = data['ticket'][key]["Xe Ô tô"]
                del data['ticket'][key]["Xe Ô tô"]
                data['ticket'][key][1] = data['ticket'][key]["Xe máy"]
                del data['ticket'][key]["Xe máy"]
            data_return.append(handle_show_data(data['ticket'][key]))
    return data_return


@app.route("/hello", methods=['GET'])
def hello():
    return "hello fitznguyen"


@app.route('/dothi')
def bokeh():
    global data_received
    import logging
    logging.warn("data %s" % data_received)
    div = handle_data_recieved(data_received)
    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    titles = ["Biểu đồ thống kê số lượng chuyến bay trong ngày"]
    # render template
    html = render_template(
        'index.html',
        titles=titles,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)


if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)
