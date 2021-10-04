from netdriving.msg import perception_msg
import numpy as np
import math as m

MSG_LENGTH_PER_VEHICLE = 35


def create_arena_msg(arena_params):
    msg = {
        "object_id":"",
        "persist": arena_params["persist"],
        "type": arena_params["type"],
        "action": arena_params["action"],
        "data": {
            "rotation": {
                "x": arena_params["rotation"][0],
                "y": arena_params["rotation"][1],
                "z": arena_params["rotation"][2]
            },
            "scale": {
                "x": arena_params["scale"][0],
                "y": arena_params["scale"][1],
                "z": arena_params["scale"][2]
            },
            "color": arena_params["color"]
        }
    }

    return msg


def tf(position, x_angle, y_angle, z_angle):
    x = position['x']
    y = position['y']
    z = position['z']

    x_rad = m.radians(x_angle)
    y_rad = m.radians(y_angle)
    z_rad = m.radians(z_angle)

    xyz = np.matrix([[x], 
                     [y], 
                     [z]])
    
    Rx = np.matrix([[ 1,            0,            0],
                    [ 0, m.cos(x_rad),-m.sin(x_rad)],
                    [ 0, m.sin(x_rad), m.cos(x_rad)]])
    
    Ry = np.matrix([[ m.cos(y_rad), 0, m.sin(y_rad)],
                    [            0, 1,            0],
                    [-m.sin(y_rad), 0, m.cos(y_rad)]])
    
    Rz = np.matrix([[ m.cos(z_rad), -m.sin(z_rad), 0],
                    [ m.sin(z_rad),  m.cos(z_rad), 0],
                    [            0,             0, 1]])
    
    rot_m = np.dot(Rx, np.dot(Ry, Rz))
    # rot_m = Rz * Ry * Rx

    result = np.dot(rot_m, xyz)

    return {'x': result.item(0,0),
            'y': result.item(1,0),
            'z': result.item(2,0)}


def arena_create_object(object_type, arena_params, arena_msg, obj_id, position=None, path=None):
    arena_msg["object_id"] = "vehicle_" + str(obj_id)
    arena_msg["data"]["object_type"] = object_type

    if object_type == 'box':
        if position != None:
            return arena_box_msg(arena_params, arena_msg, obj_id, position)
        else:
            raise ValueError("box object should be given position")

    if object_type == 'circle':
        if position != None:
            return arena_circle_msg(arena_params, arena_msg, obj_id, position)
        else:
            raise ValueError("circle object should be given position")

    if object_type == 'thickline':
        if path != None:
            return arena_thickline_msg(arena_params, arena_msg, obj_id, path)
        else:
            raise ValueError("thickline object should be given path")


def arena_box_msg(arena_params, arena_msg, obj_id, position):
    arena_msg["data"]["depth"] = arena_params["box_dimension"][0]
    arena_msg["data"]["height"] = arena_params["box_dimension"][1]
    arena_msg["data"]["width"] = arena_params["box_dimension"][2]
    arena_msg["data"]["position"] = position
    
    return arena_msg


def arena_circle_msg(arena_params, arena_msg, obj_id, position):
    arena_msg["data"]["radius"] = arena_params["circle_radius"]
    arena_msg["data"]["position"] = position
    
    return arena_msg


def arena_thickline_msg(arena_params, arena_msg, obj_id, path):
    arena_msg["data"]["lineWidth"] = arena_params["line_width"]
    arena_msg["data"]["lineWidthStyler"] = arena_params["lineWidthStyler"]

    arena_msg["data"]["path"] = path
    
    return arena_msg


def getBondingBoxVertex(bounding_box):
    vertex_list = []
    for i in range(0, 24, 3):
        vertex_list.append(bounding_box[i:i+3])

    return vertex_list


def get_num_vehicle(perception_msg):
    return perception_msg.number_of_vehicles


def get_position(perception_data, vehicle_id):
    vehicle_index = MSG_LENGTH_PER_VEHICLE * vehicle_id
    return {"x": perception_data[vehicle_index + 1],
            "y": perception_data[vehicle_index + 2],
            "z": perception_data[vehicle_index + 3]}
