import socket, select, logging, time

from unit import Unit
from api.ev3 import Ev3

class Ev3Exception(Exception):
    pass

class MockBot(Ev3):
    def __init__(self, ip_adress):
        # everything for the interal logger
        self._logger = logging.getLogger('Brick_logger')
        self._logger.setLevel(logging.WARNING)
        self._console_handler = logging.StreamHandler()
        self._console_handler.setLevel(logging.NOTSET)
        self._formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self._console_handler.setFormatter(self._formatter)
        self._logger.addHandler(self._console_handler)

        # everything for the ev3 connection
        self._logger.info("starting setup")
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._port = 1337
        socket.inet_aton(ip_adress)
        self._ip_adress = ip_adress
        self._package_size = 512
        self._timeout = 5
        self._s.settimeout(1)
        #self._s.connect((self._ip_adress, self._port))
        print('socket: connect')
        self._s.setblocking(0)
        self._motors = {}
        self._sensors_supported = {"touch": Touch, "IR": IR, "color": Color, "compass": Compass,
                                   "accelerometer": TiltSensor}
        self._sensors = {}
        self._logger.info("setup complete")

    def enable_debugging(self):
        self._logger.setLevel(logging.INFO)

    def receive_data(self):
        self._logger.info("entered receive_data")
        readable, writable, exceptional = select.select([self._s], [self._s], [self._s])
        complete_data_set = ""
        while not complete_data_set:
            self._logger.info("waiting for data to receive")
            start_time = time.time()
            while self._s not in readable:
                readable, writable, exceptional = select.select([self._s], [self._s], [self._s])
                if time.time() > start_time + self._timeout:
                    raise Ev3Exception(
                        "the ev3 did not respond within the current timeout. Solution: try again with logging set to INFO")
            if self._s in readable:
                self._logger.info("receiving data")
                print('socket: receive data')
                while self._s in readable:
                    data = self._s.recv(self._package_size).decode()
                    if not data:
                        self._logger.warning("broken connection")
                        raise socket.error
                    complete_data_set = complete_data_set + data
                    readable, writable, exceptional = select.select([self._s], [self._s], [self._s])
        self._logger.info("transfer complete,received:" + complete_data_set)
        return complete_data_set

    def disconnect(self):
        self._logger.info("entered disconnect")
        self._s.close()
        self._logger.info("socket closed")

    def get_battery_voltage(self):
        self._logger.info("entered get_battery_voltage")
        self.send_command("get_battery_voltage=")
        success, value = self.handle_respons()
        return value

    def get_battery_current(self):
        self._logger.info("entered get_battery_current")
        self.send_command("get_battery_current=")
        success, value = self.handle_respons()
        return value

    def send_data(self, data):
        self._logger.info("entered send_data,sending: " + data)
        readable, writable, exceptional = select.select([self._s], [self._s], [])
        while self._s not in writable:
            readable, writable, exceptional = select.select([self._s], [self._s], [])
        #self._s.sendall(data.encode())
        print('socket: sendall')
        self._logger.info("send complete")

    def is_digit(self, element):
        try:
            int(element)
            return True
        except ValueError:
            return False

    def is_float(self, element):
        try:
            float(element)
            return True
        except ValueError:
            return False

    def check_subelement(self, subelement):
        if self.is_digit(subelement):
            return int(subelement)
        elif self.is_float(subelement):
            return float(subelement)
        else:
            if subelement == "True":
                return True
            elif subelement == "False":
                return False
            else:
                return subelement

    # converts the string received from the host to a usable list of lists
    def convert_sensorlist(self, data):
        self._logger.info("entered convert_sensorlist")
        self._logger.info("converting: " + data)
        sensorlist = []
        data = data.split(";")
        for element in data:
            if not element: continue
            tempList = []
            temp = element.split("=")
            tempList.append(temp[0])
            temp = temp[1].split(",")
            tempList.append([])
            for subElement in temp:
                tempList[1].append(self.check_subelement(subElement))
            sensorlist.append(tempList)
        self._logger.info("convert complete: " + str(sensorlist))
        return sensorlist

    # all commands go by this method if we wan to buffer the later on and send them all together
    def send_command(self, data):
        print(data)
        self._logger.info("entered send_command,sending: " + data)
        self.send_data(data + ";")
        self._logger.info("send complete")

    def handle_respons(self):
        self._logger.info("entered handle_respons")
        #respons = self.convert_sensorlist(self.receive_data())
        respons = [ ['respons', 
                     [True, 'who knows']] ]
        self._logger.info("received: " + str(respons))
        if len(respons) != 1:
            raise Ev3Exception("responslist had more the one elements, that should not happen: " + str(respons))
        respons = respons[0]
        if respons[0] != "respons":
            raise Ev3Exception("incorrect responsform: " + str(respons))
        respons = respons[1]
        if type(respons[0]) != bool:
            raise Ev3Exception("respons does not contain a bool telling if the operation was succesful or not")
        if not respons[0] and not (type(respons[1]) == str or type(respons[1]) == unicode):
            print(type(respons[1]))
            raise Ev3Exception("respons was unsuccessful and does not contain a string telling why")
        if len(respons) == 1:
            respons.append("")
        if len(respons) > 2:
            self._logger.info("respons longer than normal")
            temp = []
            for i in range(1, len(respons)):
                temp.append(respons[i])
            return respons[0], temp
        return respons

    def get_supported_sensors(self):
        to_return = ""
        for element in self._sensors_supported:
            to_return = to_return + element + ","
        return to_return[:-1]

    def get_sensor_from_type(self, sensortype):
        self._logger.info("entered get_sensor_from_name")
        if not type(sensortype) == str:
            raise TypeError("sensortype needs to be a string")
        try:
            self._sensors_supported[sensortype]
        except KeyError:
            raise ValueError(
                "sensortype not supported, might be a misspelling. This device supports the following sensors: " + self.get_supported_sensors())
        number_of_sensors_found = 0
        sensor = None
        for element in self._sensors:
            if self._sensors[element]._type == sensortype:
                number_of_sensors_found += 1
                sensor = self._sensors[element]
        if number_of_sensors_found == 0:
            raise Ev3Exception("no sensor of type " + sensortype + " found")
        elif number_of_sensors_found > 1:
            raise Ev3Exception("more than on sensor of type " + sensortype + " found. Use get_sensor_from_port instead")
        self._logger.info("successfully retrieved sensor of type " + sensortype)
        return sensor

    def get_sensor_from_port(self, port):
        self._logger.info("entered get_sensor_from_port")
        error = False
        if not type(port) == int:
            raise TypeError("sensorport needs to be a integer")
        if port not in [1, 2, 3, 4]:
            raise ValueError("sensorport needs to be 1,2,3 or 4")
        try:
            self._sensors[port]
        except KeyError:
            error = True
        if error:
            raise ValueError("No sensor added on port " + str(port))
        self._logger.info("successfully retrieved sensor on port " + str(port))
        return self._sensors[port]

    def add_sensor(self, port, sensortype):
        self._logger.info("entered add_sensor")
        if not type(port) == int:
            raise TypeError("sensorport needs to be a integer")
        if not type(sensortype) == str:
            raise TypeError("sensortype needs to be a string")
        try:
            self._sensors_supported[sensortype]
        except KeyError:
            raise ValueError(
                "sensortype not supported, might be a misspelling. This device supports the following sensors: " + self.get_supported_sensors())

        if port not in [1, 2, 3, 4]:
            raise ValueError("sensorport needs to be 1,2,3 or 4")
        self.send_command("add_sensor=" + str(port) + "," + sensortype)
        success, value = self.handle_respons()
        if not success:
            raise Ev3Exception(str(value))
        else:
            self._sensors[port] = self._sensors_supported[sensortype](port, self)
            self._logger.info("successfully added a sensor of type " + sensortype + " on port " + str(port))
            return self._sensors[port]

    def add_motor(self, port):
        self._logger.info("entered add_motor")
        if not type(port) == str:
            raise TypeError("motorport needs to be a string")
        if port not in ["A", "B", "C", "D"]:
            raise ValueError("motorport needs to be A,B,C or D")
        self.send_command("add_motor=" + str(port))
        success, value = self.handle_respons()
        if not success:
            raise Ev3Exception(str(value))
        else:
            self._motors[port] = Motor(port, self)
            return self._motors[port]

    def get_motor(self, port):
        no_motor_error = False
        self._logger.info("entered get_motor")
        if not type(port) == str:
            raise TypeError("motorport needs to be a string")
        if port not in ["A", "B", "C", "D"]:
            raise ValueError("motorport needs to be A,B,C or D")
        try:
            self._motors[port]
        except KeyError:
            no_motor_error = True
        if no_motor_error:
            raise Ev3Exception(
                "no motor added to that port. Solution: add 'add_motor('" + port + "')' to your code before this")
        self._logger.info("motor successfully found")
        return self._motors[port]

    def start_motors(self, motors):
        self._logger.info("entered start_motors")
        if type(motors) != list:
            raise Ev3Exception("argument must be a list")
        temp = "start_motors="
        added = []
        for element in motors:
            if element not in ["A", "B", "C", "D"]:
                raise Ev3Exception(str(element) + " is not a valid motorport. Motorport must be A,B,C or D")
            if element in added:
                raise Ev3Exception("you should not add a motor twice")
            temp += element + ","
            added.append(element)
        temp = temp[:-1]
        self.send_command(temp)
        success, value = self.handle_respons()
        if not success:
            raise Ev3Exception(value)

    def stop_motors(self, motors):
        self._logger.info("entered start_motors")
        if type(motors) != list:
            raise Ev3Exception("argument must be a list")
        temp = "stop_motors="
        added = []
        for element in motors:
            if element not in ["A", "B", "C", "D"]:
                raise Ev3Exception(str(element) + " is not a valid motorport. Motorport must be A,B,C or D")
            if element in added:
                raise Ev3Exception("you should not add a motor twice")
            temp += element + ","
            added.append(element)
        temp = temp[:-1]
        self.send_command(temp)
        success, value = self.handle_respons()
        if not success:
            raise Ev3Exception(value)

    def start_all_motors(self):
        self._logger.info("entered start_all_motors")
        self.send_command("start_all_motors=")
        success, value = self.handle_respons()

    def stop_all_motors(self):
        self._logger.info("entered stop_all_motors")
        self.send_command("stop_all_motors=")
        success, value = self.handle_respons()

    def speak(self, speech):
        if type(speech) != str:
            raise Ev3Exception("must be a string")
        self.send_command("speak=" + speech)
        success, value = self.handle_respons()

    def play_wav(self, sound):
        if type(sound) != str:
            raise Ev3Exception("must be a string")
        self.send_command("play_wav=" + sound)
        success, value = self.handle_respons()
        if success:
            return value
        else:
            raise Ev3Exception(value)

    def stop_sound(self):
        self.send_command("stop_sound=")
        success, value = self.handle_respons()


class Color():
    def __init__(self, port, ev3_connection):
        self._port = port
        self._ev3 = ev3_connection
        self._type = "color"

    def get_rgb(self):
        self._ev3.send_command("sensor_color_rgb=" + str(self._port) + "," + self._type)
        success, value = self._ev3.handle_respons()
        if success:
            self._ev3._logger.info("successfully retrieved value for sensor on port: " + str(self._port))
            return value
        else:
            self._ev3._logger.info("unsuccessfully retrieved value for sensor on port: " + str(self._port))
            raise Ev3Exception("unable to retrieve value")

    def get_color(self):
        self._ev3.send_command("sensor_color_color=" + str(self._port) + "," + self._type)
        success, value = self._ev3.handle_respons()
        if success:
            self._ev3._logger.info("successfully retrieved value for sensor on port: " + str(self._port))
            return value
        else:
            self._ev3._logger.info("unsuccessfully retrieved value for sensor on port: " + str(self._port))
            raise Ev3Exception("unable to retrieve value")

    def get_reflect(self):
        self._ev3.send_command("sensor_color_reflect=" + str(self._port) + "," + self._type)
        success, value = self._ev3.handle_respons()
        if success:
            self._ev3._logger.info("successfully retrieved value for sensor on port: " + str(self._port))
            return value
        else:
            self._ev3._logger.info("unsuccessfully retrieved value for sensor on port: " + str(self._port))
            raise Ev3Exception("unable to retrieve value")

    def get_ambient(self):
        self._ev3.send_command("sensor_color_ambient=" + str(self._port) + "," + self._type)
        success, value = self._ev3.handle_respons()
        if success:
            self._ev3._logger.info("successfully retrieved value for sensor on port: " + str(self._port))
            return value
        else:
            self._ev3._logger.info("unsuccessfully retrieved value for sensor on port: " + str(self._port))
            raise Ev3Exception("unable to retrieve value")

    def get_mode(self):
        self._ev3.send_command("sensor_get_mode=" + str(self._port) + "," + self._type)
        success, value = self._ev3.handle_respons()
        if success:
            self._ev3._logger.info("successfully retrieved mode for sensor on port: " + str(self._port))
            return value
        else:
            self._ev3._logger.info("unsuccessfully retrieved mode for sensor on port: " + str(self._port))
            raise Ev3Exception("unable to retrieve mode")


class Touch():
    def __init__(self, port, ev3_connection):
        self._port = port
        self._ev3 = ev3_connection
        self._type = "touch"

    def is_pressed(self):
        self._ev3.send_command("sensor_get_value=" + str(self._port) + "," + self._type)
        success, value = self._ev3.handle_respons()
        if success:
            self._ev3._logger.info("successfully retrieved value for sensor on port: " + str(self._port))
            return value
        else:
            self._ev3._logger.info("unsuccessfully retrieved value for sensor on port: " + str(self._port))
            raise Ev3Exception("unable to retrieve value")


class Compass():
    def __init__(self, port, ev3_connection):
        self._port = port
        self._ev3 = ev3_connection
        self._type = "compass"

    def get_direction(self):
        self._ev3.send_command("sensor_compass=" + str(self._port) + "," + self._type)
        success, value = self._ev3.handle_respons()
        if success:
            self._ev3._logger.info("successfully retrieved value for sensor on port: " + str(self._port))
            return value
        else:
            self._ev3._logger.info("unsuccessfully retrieved value for sensor on port: " + str(self._port))
            raise Ev3Exception("unable to retrieve value")


class TiltSensor():
    def __init__(self, port, ev3_connection):
        self._port = port
        self._ev3 = ev3_connection
        self._type = "accelerometer"

    def get_tilt(self):
        self._ev3.send_command("sensor_accelerometer_tilt=" + str(self._port) + "," + self._type)
        success, value = self._ev3.handle_respons()
        if success:
            self._ev3._logger.info("successfully retrieved value for sensor on port: " + str(self._port))
            return value
        else:
            self._ev3._logger.info("unsuccessfully retrieved value for sensor on port: " + str(self._port))
            raise Ev3Exception("unable to retrieve value")


class IR():
    def __init__(self, port, ev3_connection):
        self._port = port
        self._ev3 = ev3_connection
        self._type = "IR"

    def get_prox(self):
        self._ev3.send_command("sensor_IR_prox=" + str(self._port) + "," + self._type)
        success, value = self._ev3.handle_respons()
        if success:
            self._ev3._logger.info("successfully retrieved value for sensor on port: " + str(self._port))
            return value
        else:
            self._ev3._logger.info("unsuccessfully retrieved value for sensor on port: " + str(self._port))
            raise Ev3Exception("unable to retrieve value")

    def get_remote(self):
        self._ev3.send_command("sensor_IR_remote=" + str(self._port) + "," + self._type)
        success, value = self._ev3.handle_respons()
        if success:
            self._ev3._logger.info("successfully retrieved value for sensor on port: " + str(self._port))
            return value
        else:
            self._ev3._logger.info("unsuccessfully retrieved value for sensor on port: " + str(self._port))
            raise Ev3Exception("unable to retrieve value")

    def get_remote_bin(self):
        self._ev3.send_command("sensor_IR_remote_bin=" + str(self._port) + "," + self._type)
        success, value = self._ev3.handle_respons()
        if success:
            self._ev3._logger.info("successfully retrieved value for sensor on port: " + str(self._port))
            return value
        else:
            self._ev3._logger.info("unsuccessfully retrieved value for sensor on port: " + str(self._port))
            raise Ev3Exception("unable to retrieve value")

    def get_seek(self):
        self._ev3.send_command("sensor_IR_seek=" + str(self._port) + "," + self._type)
        success, value = self._ev3.handle_respons()
        if success and len(value) == 8:
            self._ev3._logger.info("successfully retrieved value for sensor on port: " + str(self._port))
            temp = []
            for i in range(4):
                temp.append((value[i * 2], value[i * 2 + 1]))
            return temp
        else:
            self._ev3._logger.info("unsuccessfully retrieved value for sensor on port: " + str(self._port))
            raise Ev3Exception("unable to retrieve value")

    def get_mode(self):
        self._ev3.send_command("sensor_get_mode=" + str(self._port) + "," + self._type)
        success, value = self._ev3.handle_respons()
        if success:
            self._ev3._logger.info("successfully retrieved mode for sensor on port: " + str(self._port))
            return value
        else:
            self._ev3._logger.info("unsuccessfully retrieved mode for sensor on port: " + str(self._port))
            raise Ev3Exception("unable to retrieve mode")


class Motor():
    def __init__(self, port, ev3_connection):
        self._port = port
        self._ev3 = ev3_connection
        # att:[type,read_only]
        self._attributes = {"commands": [str, True], "command": [str, False], "reset": [str, False],
                            "count_per_rot": [int, True], "driver_name": [str, True],
                            "duty_cycle": [int, True], "duty_cycle_sp": [int, False], "encoder_polarity": [str, False],
                            "polarity_mode": [str, False]
            , "port_name": [str, False], "position": [int, False], "position_sp": [int, False],
                            "ramp_down_sp": [int, False], "ramp_up_sp": [int, False],
                            "speed": [int, True], "speed_regulation": [bool, False], "speed_sp": [int, False],
                            "state": [str, True], "stop_command": [str, False],
                            "stop_commands": [str, True], "time_sp": [int, False], "uevent": [str, True],
                            "mode": [str, False]}
        self._mode = self.get_attribute("mode")
        self._ev3._logger.info("motor successfully created")

    def change_attribute(self, att, arg):
        self._ev3._logger.info("entered change_attribute for motor on port: " + self._port)
        if type(att) != str:
            raise Ev3Exception("the attributename needs to be a string")
        try:
            self._attributes[att]
        except KeyError:
            raise Ev3Exception("no motorattribute with that name")
        if self._attributes[att][1]:
            raise Ev3Exception("attribute " + att + " is of type read-only")
        if type(arg) != self._attributes[att][0]:
            raise Ev3Exception(
                "motorattributetype is wrong, attribute " + att + " is of " + str(self._attributes[att][0]))
        self._ev3.send_command("motor_change_attribute=" + self._port + "," + str(att) + "," + str(arg))
        success, value = self._ev3.handle_respons()
        if success:
            self._ev3._logger.info("succesfully changed attribute for motor on port: " + self._port)
        else:
            self._ev3._logger.info("unsuccesfully changed attribute for motor on port: " + self._port)

    def change_attributes(self, attlist):
        print(self._port, attlist)
        command = "motor_change_attributes=" + self._port
        for element in attlist:
            att = element[0]
            arg = element[1]
            if type(att) != str:
                raise Ev3Exception("the attributename needs to be a string")
            try:
                self._attributes[att]
            except KeyError:
                raise Ev3Exception("no motorattribute with the name of " + att)
            if self._attributes[att][1]:
                raise Ev3Exception("attribute " + att + " is of type read-only")
            if type(arg) != self._attributes[att][0]:
                raise Ev3Exception(
                    "motorattributetype is wrong, attribute " + att + " is of " + str(self._attributes[att][0]))
            command = command + "," + att + "," + str(arg)
        self._ev3.send_command(command)
        success, value = self._ev3.handle_respons()
        if success:
            self._ev3._logger.info("succesfully changed attributes for motor on port: " + self._port)
        else:
            self._ev3._logger.info("unsuccesfully changed attribute for motor on port: " + self._port)

    def get_attribute(self, att):
        self._ev3._logger.info("entered get_attribute for motor on port: " + self._port)
        if type(att) != str:
            raise Ev3Exception("the attributename needs to be a string")
        try:
            self._attributes[att]
        except KeyError:
            raise Ev3Exception("no motorattribute with that name")
        self._ev3.send_command("motor_get_attribute=" + self._port + "," + att)
        success, value = self._ev3.handle_respons()
        if success:
            self._ev3._logger.info("successfully retrieved attribute for motor on port: " + self._port)
            return value
        else:
            self._ev3._logger.info("unsuccessfully retrieved attribute for motor on port: " + self._port)
            raise Ev3Exception("unable to retrieve attribute")

    def run_time_limited(self, speed, time_to_run, brake="coast", run=True, finish=False):
        if type(speed) != int:
            raise Ev3Exception(
                "speed here can only be expressed in integers, might you perhaps be using floats? in that case int(value) might save you")
        if abs(speed) > 100:
            raise Ev3Exception(
                "ludicrous speed not available, the absolute of the speed value must be smaller or equal to 100")
        if type(time_to_run) != int:
            raise Ev3Exception(
                "time here can only be expressed in integers, might you perhaps be using floats? in that case int(value) might save you")
        if type(run) != bool or type(finish) != bool:
            raise Ev3Exception("srsly")
        if time_to_run < 0:
            raise Ev3Exception(
                "time cant be negative. But after your physicscourse you might be able to build a flux capacitor and who knows what will happen then")
        if brake not in ["coast", "brake", "hold"]:
            raise Ev3Exception("that is not a valid brakeoption")
        if self.get_attribute("mode") != "run-timed":
            self.reset()
        temp = [["mode", "run-timed"]]
        temp.append(["speed_regulation", True])
        # if self.get_attribute("speed_regulation"):
        speed *= 9
        temp.append(["speed_sp", speed])
        # else:
        #     temp.append(["duty_cycle_sp", speed])
        temp.append(["time_sp", time_to_run])
        temp.append(["stop_command", brake])
        if run:
            temp.append(["command", "run-timed"])
        self.change_attributes(temp)
        if finish and run:
            while self.get_attribute("state") == "running":
                time.sleep(0.001)

    def run_position_limited(self, speed, position, brake="coast", run=True, absolute=True, finish=False):
        if type(speed) != int:
            raise Ev3Exception(
                "speed here can only be expressed in integers, might you perhaps be using floats? in that case int(value) might save you")
        if abs(speed) > 100:
            raise Ev3Exception(
                "ludicrous speed not available, the absolute of the speed value must be smaller or equal to 100")
        speed *= 9
        if type(position) != int:
            raise Ev3Exception(
                "position here can only be expressed in integers, might you perhaps be using floats? in that case int(value) might save you")
        if type(run) != bool or type(absolute) != bool or type(finish) != bool:
            raise Ev3Exception("srsly")
        if brake not in ["coast", "brake", "hold"]:
            raise Ev3Exception("that is not a valid brakeoption")
        temp_mode = self.get_attribute("mode")
        self.reset()
        temp = []
        temp_string = ""
        if absolute:
            temp.append(["mode", "run-to-abs-pos"])
            temp_string = "run-to-abs-pos"
        else:
            temp.append(["mode", "run-to-rel-pos"])
            temp_string = "run-to-rel-pos"
        polarity = 1
        if speed != 0 and position != 0:
            polarity = (speed / abs(speed)) * (position / abs(position))
        speed = abs(speed)
        position = abs(position)
        position = int(polarity * position)
        temp.append(["speed_regulation", True])
        temp.append(["speed_sp", speed])
        temp.append(["position_sp", position])
        temp.append(["stop_command", brake])
        if run:
            temp.append(["command", temp_string])
        self.change_attributes(temp)
        if finish and run:
            while self.get_attribute("state") == "running":
                time.sleep(0.001)

    def start(self):
        self.change_attributes([["command", self.get_attribute("mode")]])

    def stop(self):
        self.change_attributes([["mode", "stop"]])
        self.change_attributes([["command", "stop"]])

    def reset(self):
        self.change_attributes([["reset", "reset"]])

    def is_running(self):
        return self.get_attribute("state")!=""

    def run_forever(self, speed, run=True):
        if type(speed) != int:
            raise Ev3Exception(
                "speed here can only be expressed in integers, might you perhaps be using floats? in that case int(value) might save you")
        if abs(speed) > 100:
            raise Ev3Exception(
                "ludicrous speed not available, the absolute of the speed value must be smaller or equal to 100")
        if type(run) != bool:
            raise Ev3Exception("srsly")
        if self.get_attribute("mode") != "run-forever":
            self.reset()
        temp = [["mode", "run-forever"]]
        # if self.get_attribute("speed_regulation"):
        temp.append(["speed_regulation", True])
        temp.append(["speed_sp", speed * 9])
        # else:
        #     temp.append(["duty_cycle_sp", speed])
        if run:
            temp.append(["command", "run-forever"])
        self.change_attributes(temp)

class MockedEv3(Unit, MockBot): pass
