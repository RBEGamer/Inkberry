import io
import multiprocessing
import os
import time
from datetime import datetime
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
import flask
from flask import Flask, request, jsonify, make_response, redirect, render_template, g, send_file
from waitress import serve
from flask_cors import CORS, cross_origin
import bleach
import typer
import pathlib
from DisplayFramework import Devices, SVGRenderer, SVGTemplates, DeviceSpecification, BaseTile, ImplementedDevices, DeviceLookUpTable
from DisplayFramework.TileSpecification import TileSpecification

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


@app_flask.route('/favicon.ico')
def favicon_redirect():  # put application's code here
    return redirect('/{}/favicon.ico'.format(STATIC_FOLDER_NAME))


@app_flask.route('/api/list_devices', methods=['GET', 'POST'])
def api_list_devices():
    ret: dict = {}
    ret['devices'] = Devices.Devices.GetRegisteredDeviceIds(True)
    return jsonify(ret)

@app_flask.route('/api/list_display_orientations', methods=['GET', 'POST'])
def api_display_orientations():
    ret: dict = {}
    ret['orientations'] = []

    for orientation in DeviceSpecification.DisplayOrientation:
        ret['orientations'].append({'name': orientation.name, 'value': orientation.value})
    return jsonify(ret)

@app_flask.route('/api/list_hardware_types', methods=['GET', 'POST'])
def api_list_hardware_types():
    ret: dict = {}
    ret['hardware_type'] = []

    for device in ImplementedDevices.ImplementedDevices:
        ret['hardware_type'].append({'name': device.name, 'id': device.value})
    return jsonify(ret)


@app_flask.route('/api/get_hardware_type_name/<string:hardware_type>', methods=['GET', 'POST'])
def api_get_hardware_type_name(hardware_type: str):
    hardware_type = bleach.clean(hardware_type).strip(' ').strip('/')

    try:
        hardware_type_int: int = int(hardware_type)

        return jsonify({"hardware_type_name": ImplementedDevices.ImplementedDevices.from_int(hardware_type_int).name, "error": None, "hardware_type": hardware_type, "hardware_type_int": hardware_type_int}), 200
    except ValueError:
        return jsonify({"hardware_type_name": "INVALID", "error": "hardware_type_parameter_invalid_or_not_found", "hardware_type": hardware_type}), 200

@app_flask.route('/api/imageapi/<path:image>', methods=['GET', 'POST'])
def imageapi(image: str):
    image = bleach.clean(image).strip(' ').strip('/')

    # ALWAYS RETURN AN SCREEN :)
    # TODO REMOVE HANDLE ERRORS
    device_spec: DeviceSpecification.DeviceSpecification = None
    image_type: str = None
    image_id: str = None
    if len(image) <= 0 or '.' not in image:
        hardware_type: ImplementedDevices.ImplementedDevices = ImplementedDevices.ImplementedDevices.MINIMAL
        device_spec = DeviceLookUpTable.DeviceLookUpTable.get_hardware_definition(hardware_type)
        image_id = device_spec.device_id
        image_type = 'bmp'
    else:

        spr: [str] = image.split(".")
        image_id = spr[0]
        image_type = spr[1].lower()

        if Devices.Devices.CheckDeviceExists(image_id):
            device_spec = Devices.Devices.GetDeviceSpecification(image_id)
        else:
            return jsonify({"error": "invalid id"}), 200

    return generate_rendered_screen_response(image_id, device_spec, image_type, 0 , False, request)


@app_flask.route('/api/set_delete_display/<string:device_id>', methods=['GET', 'POST'])
def set_delete_display(device_id: str):
    device_id = bleach.clean(device_id)

    if not Devices.Devices.CheckDeviceExists(device_id):
        return jsonify({"CheckDeviceExistsFailed": None}), 500
    else:
        Devices.Devices.DeleteDevice(device_id)
        return jsonify({"error": None}), 200

@app_flask.route('/api/set_display_state/<string:device_id>/<string:enable_state>', methods=['GET', 'POST'])
def api_setdisplay_state(device_id: str, enable_state: str):
    device_id = bleach.clean(device_id)
    enable_state = bleach.clean(enable_state)


    if not Devices.Devices.CheckDeviceExists(device_id):
        return jsonify({"CheckDeviceExistsFailed": None}), 500
    else:
        device_spec = Devices.Devices.GetDeviceSpecification(device_id)

        if enable_state == "true" or enable_state == "1" or enable_state == "True":
            device_spec.enabled = True
        elif enable_state == "false" or enable_state == "0" or enable_state == "False":
            device_spec.enabled = False

        Devices.Devices.UpdateDeviceSpecification(device_spec)

        return jsonify({"error": None}), 200


@app_flask.route(
    '/api/update_parameter/<string:device_id>/<string:tile_id>/<string:parameter_id>/<string:value>/<string:is_system_parameter>', methods=['GET', 'POST'])
def api_update_parameter(device_id: str, tile_id: str, parameter_id: str, value: str, is_system_parameter: str):
    device_id = bleach.clean(device_id)
    tile_id = bleach.clean(tile_id)
    parameter_id = bleach.clean(parameter_id)
    value = bleach.clean(value)

    try:
        is_system_parameter = bool(int(bleach.clean(is_system_parameter)))
    except Exception:
        is_system_parameter = False

    ret = {"error": None}
    if not Devices.Devices.CheckDeviceExists(device_id):
        ret.update({'error': 'invalid_device'})
    else:
        device_spec: DeviceSpecification.DeviceSpecification = Devices.Devices.GetDeviceSpecification(device_id)

        # TODO REWORK DICT
        for idx, tile in enumerate(device_spec.tile_specifications):
            if tile_id == tile.name:

                if is_system_parameter:
                    try:
                        if parameter_id == "enabled":
                            if value == "true" or value == "1" or value == "True":
                                device_spec.tile_specifications[idx].enabled = True
                            elif value == "false" or value == "0" or value == "False":
                                device_spec.tile_specifications[idx].enabled = False
                        elif parameter_id == "position_x":
                            device_spec.tile_specifications[idx].position.pos_x = int(value)
                        elif parameter_id == "position_y":
                            device_spec.tile_specifications[idx].position.pos_y = int(value)

                    except Exception:
                        pass
                else:
                    if parameter_id in device_spec.tile_specifications[idx].parameters:
                        device_spec.tile_specifications[idx].parameters[parameter_id] = value
                break

        Devices.Devices.UpdateDeviceSpecification(device_spec)

    return jsonify(ret)


@app_flask.route('/api/get_tiles_list/<string:device_id>', methods=['GET', 'POST'])
def api_get_tiles_list(device_id: str):
    device_id = bleach.clean(device_id)
    tiles: [str] = []
    ret = {"error": None, 'tiles': []}

    ret = {"error": None, 'parameters': [], 'system_parameters': []}
    if not Devices.Devices.CheckDeviceExists(device_id):
        ret.update({'error': 'invalid_device'})
    else:
        device_spec = Devices.Devices.GetDeviceSpecification(device_id)
        for tile in device_spec.tile_specifications:
            tile: TileSpecification
            tiles.append({'name': tile.name, 'is_system_parameter': False})

    ret['tiles'] = tiles
    return jsonify(ret)


@app_flask.route('/api/get_parameter_list/<string:device_id>/<string:parameter_id>', methods=['GET', 'POST'])
def api_get_parameter_list(device_id: str, parameter_id: str):
    device_id = bleach.clean(device_id)
    parameter_id = bleach.clean(parameter_id)

    ret = {"error": None, 'parameters': [], 'system_parameters': []}
    if not Devices.Devices.CheckDeviceExists(device_id):
        ret.update({'error': 'invalid_device'})
    else:
        device_spec = Devices.Devices.GetDeviceSpecification(device_id)

        # TODO REWORK
        # ADD OPTIONAL PARAMETERS FROM TILE
        for tile in device_spec.tile_specifications:
            if parameter_id == tile.name:
                ret.update({'parameters': tile.parameters})

                # ADD SYSTEM PARAMETERS EQUAL FOR EACH TILE
                ret.update({'system_parameters': {'enabled': tile.enabled, 'position_x': tile.position.pos_x, 'position_y': tile.position.pos_y}})

        return jsonify(ret)




@app_flask.route('/api/list_possible_parent_devices/<string:did>/<string:devies_type>', methods=['GET', 'POST'])
def api_list_possible_parent_devices(did: str, devies_type: str):
    devies_type = bleach.clean(devies_type)
    did = bleach.clean(did)
    ret: dict = {}
    try:
        devices_enum: ImplementedDevices.ImplementedDevices = ImplementedDevices.ImplementedDevices.from_int(int(devies_type))

        # GET POSSIBLE COMPATIBLE TYPES
        possible_types: [ImplementedDevices.ImplementedDevices] = DeviceLookUpTable.DeviceLookUpTable.get_compatible_hardware_models(devices_enum)
        ret['possible_parents'] = []
        for type in possible_types:
            for rt in Devices.Devices.GetRegisteredDevicesOfHardwareType(type, did, True):
                ret['possible_parents'].append(rt)

    except Exception as e:
        ret['possible_parents'] = Devices.Devices.GetRegisteredDeviceIds(True, True)
        ret['error'] = str(e)


    return jsonify(ret)
@app_flask.route('/api/information/<string:device_id>', methods=['GET', 'POST'])
def api_information(device_id: str):
    device_id = bleach.clean(device_id)
    ret = {"error": None, 'parameter': []}

    if not Devices.Devices.CheckDeviceExists(device_id):
        ret.update({'error': 'invalid_device'})

    else:
        device_spec = Devices.Devices.GetDeviceSpecification(device_id)

        ret.update({
            'hardware': '{} [{}x{} WUP:{} ENABLED:{}]'.format(device_spec.get_hardware_type().name, device_spec.screen_size_w,
                                                   device_spec.screen_size_h, device_spec.wakeup_interval, device_spec.enabled),
            'name': '{} @ {} '.format(device_spec.allocation, device_spec.device_id),
        })

    return jsonify(ret)


@app_flask.route('/api/state/<string:did>', methods=['GET', 'POST'])
def api_state(did: str):  # put application's code here
    did = bleach.clean(did)


    if not Devices.Devices.CheckDeviceExists(bleach.clean(did)):
        return "CheckDeviceExistsFailed", 200

    if Devices.Devices.CheckForUpdatedData(bleach.clean(did)):
        return "RefreshRequired", 200

    # UPDATE STATE
    rd: dict = {}
    for k in request.args.keys():
        ks: str = bleach.clean(k)
        rd.update({ks: bleach.clean(request.args.get(k, default=''))})

    Devices.Devices.UpdateDeviceStatus(bleach.clean(did), str(datetime.now()), rd)


    return "", 200


@app_flask.route('/api/register_new/<string:did>/<string:typename>/<string:allocation>/<string:orientation>', methods=['GET', 'POST'])
def api_register_new(did: str, typename: str, allocation: str, orientation: str):  # put application's code here
    did = bleach.clean(did)
    typename = bleach.clean(typename)
    allocation = bleach.clean(allocation)
    orientation = bleach.clean(orientation)

    if not Devices.Devices.CheckDeviceExists(did):
        try:
            dorient: DeviceSpecification.DisplayOrientation = DeviceSpecification.DisplayOrientation.from_int(int(orientation))
            created_device_spec: DeviceSpecification.DeviceSpecification = Devices.Devices.CreateDeviceFromName(typename, did, _allocation=allocation, _orientation=dorient)

            if created_device_spec is None:
                return jsonify({'error': 'cant create device'}), 200

            return jsonify(created_device_spec.to_dict()), 200
        except Exception as e:
            return jsonify({'error': e}), 200

    return jsonify({'error': 'device already exists'}), 200


@app_flask.route('/api/register_parent/<string:did>/<string:typename>/<string:allocation>/<string:parent>', methods=['GET', 'POST'])
def api_register_parent(did: str, typename: str, allocation: str, parent: str):  # put application's code here
    did = bleach.clean(did)
    typename = bleach.clean(typename)
    allocation = bleach.clean(allocation)
    parent = bleach.clean(parent)

    ret = {}
    if Devices.Devices.CheckDeviceExists(parent):
        # DELETE OLD CHILD DEVICE
        if Devices.Devices.CheckDeviceExists(did):
            Devices.Devices.DeleteDevice(did)

        parent_spec: DeviceSpecification.DeviceSpecification = Devices.Devices.GetDeviceSpecification(parent)

        # CHECK TYPE
        parent_spec.device_id = did
        parent_spec.allocation = allocation
        created_device_spec = Devices.Devices.CreateDeviceFromName(typename, did, _allocation=allocation)

        if created_device_spec is None:
            return jsonify({'error': 'cant create device'}), 200


        if created_device_spec.hardware != parent_spec.hardware:
            return jsonify({'error': 'invalid hardware type, parent and child hardware revision mut match'}), 200

        # APPLY PARENTING
        created_device_spec.parent_id = parent
        Devices.Devices.UpdateDeviceSpecification(created_device_spec)

        return jsonify(created_device_spec.to_dict())
    return jsonify({'error': 'device already exists'}), 200

@app_flask.route('/api/useractonredirect/<string:did>', methods=['GET', 'POST'])
def api_useractonredirect(did: str):
    did: str = bleach.clean(did)
    hardware_type: str = bleach.clean(request.args.get('hardware_type', default='{}'.format(ImplementedDevices.ImplementedDevices.SIMULATED.value))).lower()

    if not Devices.Devices.CheckDeviceExists(bleach.clean(did)):
        return redirect('/static/register.html?did={}&hardware_type={}'.format(did, hardware_type))
    elif not Devices.Devices.CheckDeviceEnabled(did):
        return redirect('/static/reactivate.html?did={}&hardware_type={}'.format(did, hardware_type))
    else:
        return redirect('/static/index.html?did={}&hardware_type={}'.format(did, hardware_type))


@app_flask.route('/api/render/<string:did>', methods=['GET', 'POST'])
def api_render(did: str):
    did: str = bleach.clean(did)
    image_type: str = bleach.clean(request.args.get('type', default='png')).lower().strip(' ')
    hw_type: int = int(bleach.clean(request.args.get('hw', default='0')))
    force_current_screen_render: bool = bool(int(bleach.clean(request.args.get('fcsr', default='0'))))
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
    if did == "" or not Devices.Devices.CheckDeviceExists(did):
        # IF NO DEVICE IS GIVEN BUT THE HARDWARE TYPE, THEN CREATE A TEMPORARY DEVICE SPECIFICATION TO RENDER THE SETUP/ DISABLED SCREEN
        if hw_type is not None:
            hardware_type: ImplementedDevices.ImplementedDevices = ImplementedDevices.ImplementedDevices.from_int(hw_type)
            device_spec = DeviceLookUpTable.DeviceLookUpTable.get_hardware_definition(hardware_type)
    else:
        device_spec = Devices.Devices.GetDeviceSpecification(did)

    if not target_width or target_width > 0:
        target_width = target_width
    else:
        target_width = 0


    return generate_rendered_screen_response(did, device_spec, image_type, target_width, force_current_screen_render, request)


def generate_rendered_screen_response(did: str, device_spec: DeviceSpecification.DeviceSpecification, image_type: str,
                                      target_width: int = 0, _force_current_screen_render: bool = True, _origin_request: flask.Request = None) -> flask.Response:
    # GENERATE SVG IMAGE DEPENDING ON THE DISPLAY CONFIGURED STATE

    # FOR POSSIBLE QR CODES
    base_url = "https://inkberry.marcelochsendorf.com"
    if _origin_request is not None:
        hardware_type: str = bleach.clean(request.args.get('hw', default='99')).lower().strip(' ')
        base_url = "{}api/useractonredirect/{}?hardware_type={}".format(_origin_request.host_url, did, hardware_type)


    # TODO REMOVE
    # LIMIT MAX SCREEN SIZE TO ACTUAL SIZE
    if target_width > device_spec.screen_size_w:
        target_width = device_spec.screen_size_w

    if _force_current_screen_render:
        svg = SVGTemplates.SVGTemplates.GenerateCurrentDeviceScreen(did, device_spec, target_width)
    elif not device_spec.is_valid() or not Devices.Devices.CheckDeviceExists(did):
        svg = SVGTemplates.SVGTemplates.GenerateDeviceSetupScreen(did, device_spec, target_width, base_url)
    elif not Devices.Devices.CheckDeviceEnabled(did):
        svg = SVGTemplates.SVGTemplates.GenerateDeviceDisabledScreen(did, device_spec, target_width, base_url)
    else:
        svg = SVGTemplates.SVGTemplates.GenerateCurrentDeviceScreen(did, device_spec, target_width)

    # RETURN AS SVG OR PNG TO CLIENT

    if image_type == "png":
        return send_file(SVGRenderer.SVGRenderer.SVG2Image(svg, device_spec, SVGRenderer.SVG_ExportTypes.PNG),
                         mimetype='image/png')
    elif image_type == "pdf":
        return send_file(SVGRenderer.SVGRenderer.SVG2Image(svg, device_spec, SVGRenderer.SVG_ExportTypes.PDF),
                         mimetype='application/pdf')
    elif image_type == "ps":
        return send_file(SVGRenderer.SVGRenderer.SVG2Image(svg, device_spec, SVGRenderer.SVG_ExportTypes.PS),
                         mimetype='application/pdf')
    elif image_type == "eps":
        return send_file(SVGRenderer.SVGRenderer.SVG2Image(svg, device_spec, SVGRenderer.SVG_ExportTypes.EPS),
                         mimetype='application/pdf')
    elif image_type == "svg":
        return send_file(SVGRenderer.SVGRenderer.SVG2Image(svg, device_spec, SVGRenderer.SVG_ExportTypes.SVG),
                         mimetype='image/svg+xml')

    elif image_type == "jpg" or image_type == "jpeg":
        return send_file(SVGRenderer.SVGRenderer.SVG2Image(svg, device_spec, SVGRenderer.SVG_ExportTypes.JPG),
                         mimetype='image/jpeg')

    elif image_type == "calepd":
        return send_file(SVGRenderer.SVGRenderer.SVG2Image(svg, device_spec, SVGRenderer.SVG_ExportTypes.CalEPD),
                         mimetype='image/bmp')

    elif image_type == "html":
        w, h = SVGRenderer.SVGRenderer.SVGGetSize(svg)

        return redirect('/static/htmlpreview.html?did={}&w={}&h={}'.format(did, w, h))
    else:
        return send_file(SVGRenderer.SVGRenderer.SVG2Image(svg, device_spec, SVGRenderer.SVG_ExportTypes.BMP),
                         mimetype='image/bmp')


def flask_server_task(_config: dict):
    global hardware_instances
    host: str = _config.get("host", "0.0.0.0")
    port: int = _config.get("port", 55556)
    debug: bool = _config.get("dbg", False)

    app_flask.config.update(_config)

    if debug:
        app_flask.run(host=host, port=port, debug=debug)
    else:
        serve(app_flask, host=host, port=port)


@app_typer.command()
def launch(typer_ctx: typer.Context, port: int = 55556, host: str = "0.0.0.0", debug: bool = False, rendernode: bool = True):
    global terminate_flask

    sys_cfg = {
        'initialized': False
    }

    # FINALLY START FLASK
    flask_config = {"port": port, "host": host, "dbg": debug, "syscfg": sys_cfg}
    flask_server: multiprocessing.Process = multiprocessing.Process(target=flask_server_task, args=(flask_config,))
    flask_server.start()
    print("DisplayServer started. http://{}:{}/".format(host, port))


    # SETUP A SCHEDULER TO UPDATE SCREENS
    scheduler = BackgroundScheduler()



    # UPDATE SCHEDULER LIST DEPEND ON THE ENABLED DISPLAYS
    while (not terminate_flask):
        time.sleep(1)
        jobs = scheduler.get_jobs()
        registered_and_enabled_devices: [str] = Devices.Devices.GetRegisteredDeviceIds(_include_only_not_deleted=True, _include_only_enabled_devices=True)

        scheduler.add_job(update_screen_components, 'interval', seconds=3, args=[])

        i = 0
        #if typer.prompt("Terminate  [Y/n]", 'y') == 'y':
        #    break

    # STOP
    flask_server.terminate()
    flask_server.join()



def update_screen_components(_job_id: str, _device_id: str):
    pass

@app_typer.callback(invoke_without_command=True)
def main(ctx: typer.Context, basepath: str = ""):
    if basepath is not None and len(basepath) > 0:
        print("main with basepath={}".format(basepath))
        Devices.Devices.SetDatabaseFolder(str(Path(str(os.path.dirname(basepath))).joinpath("data/")))
        BaseTile.BaseTileSettings.SetResourceFolder(str(Path(str(os.path.dirname(basepath))).joinpath("resources/")))
    else:
        Devices.Devices.SetDatabaseFolder(str(pathlib.Path(__file__).parent.resolve().joinpath('data')))
        BaseTile.BaseTileSettings.SetResourceFolder(str(pathlib.Path(__file__).parent.resolve().joinpath('resources')))



def run():
    app_typer()


if __name__ == "__main__":
    run()
