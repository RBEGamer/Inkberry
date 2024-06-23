import io
import multiprocessing
import os
from datetime import datetime
from pathlib import Path


from flask import Flask, request, jsonify, make_response, redirect, render_template, g, send_file
from waitress import serve
from flask_cors import CORS, cross_origin
import bleach
import typer
import pathlib
from DisplayFramework import Devices, SVGRenderer, SVGTemplates, DeviceSpecification, BaseTile

app_typer = typer.Typer(add_completion=True)

STATIC_FOLDER_NAME: str = "static"
STATIC_FOLDER_PATH: str = str(pathlib.Path(__file__).parent.resolve().joinpath(STATIC_FOLDER_NAME))

app_flask = Flask(__name__, static_folder=STATIC_FOLDER_PATH)
cors = CORS(app_flask)
app_flask.config['CORS_HEADERS'] = 'Content-Type'
terminate_flask: bool = False


# CONFIGURE COMPONENTS
## SETUP DATABASE FILE FOR STORING DEVICES
Devices.Devices.SetDatabaseFolder(str(Path(str(os.path.dirname(__file__))).joinpath("data/")))
BaseTile.BaseTileSettings.SetResourceFolder(str(Path(str(os.path.dirname(__file__))).joinpath("resources/")))

@app_flask.errorhandler(404)
def page_not_found(e):
    return redirect("/", 404)

@app_flask.route('/')
def hello_world():  # put application's code here
    return redirect('/{}/index.html'.format(STATIC_FOLDER_NAME))


@app_flask.route('/api/list_devices')
def api_list_devices():
    ret: dict = {}
    ret['devices'] = Devices.Devices.GetRegisteredDeviceIds()
    return jsonify(ret)


@app_flask.route('/api/update_parameter/<string:device_id>/<string:tile_id>/<string:parameter_id>/<string:value>')
def api_update_parameter(device_id: str, tile_id: str, parameter_id: str ,value: str):
    device_id = bleach.clean(device_id)
    tile_id = bleach.clean(tile_id)
    parameter_id = bleach.clean(parameter_id)
    value = bleach.clean(value)

    ret = {"error": None}
    if not Devices.Devices.CheckDeviceExists(device_id):
        ret.update({'error': 'invalid_device'})
    else:
        device_spec: DeviceSpecification.DeviceSpecification = Devices.Devices.GetDeviceSpecification(device_id)

        # TODO REWORK DICT
        for idx, tile in enumerate(device_spec.tile_specifications):
            if tile_id == tile.name:
                if parameter_id in device_spec.tile_specifications[idx].parameters:
                    device_spec.tile_specifications[idx].parameters[parameter_id] = value
                break


        Devices.Devices.UpdateDeviceSpecification(device_spec)

    return jsonify(ret)
@app_flask.route('/api/get_parameter_list/<string:device_id>/<string:parameter_id>')
def api_get_parameter_list(device_id: str, parameter_id: str):
    device_id = bleach.clean(device_id)
    parameter_id = bleach.clean(parameter_id)

    ret = {"error": None, 'parameters': []}
    if not Devices.Devices.CheckDeviceExists(device_id):
        ret.update({'error': 'invalid_device'})
    else:
        device_spec = Devices.Devices.GetDeviceSpecification(device_id)

    # TODO REVIRE LIST TO DICT APPROACH WITH UNIQUE ID

        for tile in device_spec.tile_specifications:
            if parameter_id == tile.name:
                ret.update({'parameters': tile.parameters})

        return jsonify(ret)

@app_flask.route('/api/information/<string:device_id>')
def api_information(device_id: str):
    device_id = bleach.clean(device_id)
    ret = {"error": None, 'parameter': []}

    if not Devices.Devices.CheckDeviceExists(device_id):
        ret.update({'error': 'invalid_device'})

    else:
        device_spec = Devices.Devices.GetDeviceSpecification(device_id)

        ret.update({
            'hardware': '{} [{}x{} WUP:{}]'.format(device_spec.get_hardware_type().name, device_spec.screen_size_w, device_spec.screen_size_h, device_spec.wakeup_interval),
            'name': '{} [{}]'.format(device_spec.allocation, device_spec.device_id),
        })

    return jsonify(ret)



@app_flask.route('/api/state/<string:id>')
def api_state(id: str):  # put application's code here

    rd: dict = {}
    for k in request.args.keys():
        ks: str = bleach.clean(k)
        rd.update({ks: bleach.clean(request.args.get(k, default=''))})

    Devices.Devices.UpdateDeviceStatus(bleach.clean(id), str(datetime.now()), rd)


    if not Devices.Devices.CheckDeviceExists(bleach.clean(id)):
        return "CheckDeviceExistsFailed", 200

    if Devices.Devices.CheckForUpdatedData(bleach.clean(id)):
        return "RefreshRequired", 200

    return "", 200


@app_flask.route('/api/register/<id>/<string:typename>')
def api_register(id: str, typename: str):  # put application's code here
    id = bleach.clean(id)
    typename = bleach.clean(typename)

    ret = {}
    if not Devices.Devices.CheckDeviceExists(id):
        ret = Devices.Devices.CreateDeviceFromName(typename, id)

    return jsonify(ret)

@app_flask.route('/api/render/<string:id>')
def api_render(id: str):
    id: str = bleach.clean(id)
    as_png: bool = bool(int(bleach.clean(request.args.get('as_png', default='1'))))
    target_width: int = 0
    try:
        target_width = int(bleach.clean(request.args.get('target_width', default='0')))
    except Exception as e1:
        try:
            target_width = int(float(bleach.clean(request.args.get('target_width', default='0'))))
        except Exception as e2:
            pass

    # GET DEVICE RESOLUTION
    device_spec: DeviceSpecification.DeviceSpecification = None
    if id == "":
        device_spec = Devices.Devices.GetRandomDeviceRecord()
    else:
        device_spec = Devices.Devices.GetDeviceSpecification(id)

    if not target_width or  target_width > 0:
        target_width = target_width
    else:
        target_width = 0

    # GENERATE SVG IMAGE
    svg: str = ""
    if not device_spec.is_valid():
        pass
    elif not Devices.Devices.CheckDeviceExists(id):
        svg = SVGTemplates.SVGTemplates.GenerateDeviceSetupScreen(id, device_spec, target_width)
    elif not Devices.Devices.CheckDeviceEnabled(id):
        svg = SVGTemplates.SVGTemplates.GenerateDeviceDisabledScreen(id, device_spec, target_width)
    else:
        svg = SVGTemplates.SVGTemplates.GenerateCurrentDeviceScreen(id, device_spec, target_width)

    # SCALE TO DEVICE SCREEN SIZE
    # TODO target_width


    # RETURN AS SVG OR PNG TO CLIENT
    if not as_png:
        svgByteArr: io.BytesIO = io.BytesIO(svg.encode(encoding = 'UTF-8'))
        #svgByteArr.seek(0)
        return send_file(svgByteArr, mimetype="image/svg+xml")
    else:
        png_bytes: io.BytesIO = SVGRenderer.SVGRenderer.SVG2PNG(svg, _device=device_spec)
        return send_file(png_bytes, mimetype='image/png')




def flask_server_task(_config: dict):
    global hardware_instances
    host: str = _config.get("host", "0.0.0.0")
    port: int = _config.get("port", 55556)
    debug: bool = _config.get("dbg", False)

    app_flask.config.update(_config)
    #with flas
    #    flask.g.test = 0

    #app_flask.app_context().push()
    if debug:
        app_flask.run(host=host, port=port, debug=debug)
    else:
        serve(app_flask, host=host, port=port)



@app_typer.command()
def launch(typer_ctx: typer.Context, port: int = 55556, host: str = "0.0.0.0", debug: bool = False):
    global terminate_flask

    sys_cfg = {
        'initialized': False
    }

    # FINALLY START FLASK
    flask_config = {"port": port, "host": host, "dbg": debug, "syscfg": sys_cfg}
    flask_server: multiprocessing.Process = multiprocessing.Process(target=flask_server_task, args=(flask_config,))
    flask_server.start()

    while( not terminate_flask):
        print("DisplayServer started. http://{}:{}/".format(host, port))
        if typer.prompt("Terminate  [Y/n]", 'y') == 'y':
            break


    # STOP
    flask_server.terminate()
    flask_server.join()


@app_typer.callback(invoke_without_command=True)
def main(ctx: typer.Context, basepath: str = ""):
    if basepath is not None and len(basepath) > 0:
        print("main with basepath={}".format(basepath))
        Devices.Devices.SetDatabaseFolder(str(Path(str(os.path.dirname(basepath))).joinpath("data/")))
        BaseTile.BaseTileSettings.SetResourceFolder(str(Path(str(os.path.dirname(basepath))).joinpath("resources/")))
    else:
        Devices.Devices.SetDatabaseFolder(str(pathlib.Path(__file__).parent.resolve().joinpath('data')))
        BaseTile.BaseTileSettings.SetResourceFolder(str(pathlib.Path(__file__).parent.resolve().joinpath('resources')))

    Devices.Devices.CreateDevice(Devices.ImplementedDevices.ImplementedDevices.ARDUINO_ESP32_7_5_INCH, "boom")
def run():
    app_typer()



if __name__ == "__main__":
    run()