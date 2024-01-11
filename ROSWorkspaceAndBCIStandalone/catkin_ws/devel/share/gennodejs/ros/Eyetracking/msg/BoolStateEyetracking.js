// Auto-generated. Do not edit!

// (in-package Eyetracking.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class BoolStateEyetracking {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.bool_data = null;
      this.int_data = null;
    }
    else {
      if (initObj.hasOwnProperty('bool_data')) {
        this.bool_data = initObj.bool_data
      }
      else {
        this.bool_data = false;
      }
      if (initObj.hasOwnProperty('int_data')) {
        this.int_data = initObj.int_data
      }
      else {
        this.int_data = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type BoolStateEyetracking
    // Serialize message field [bool_data]
    bufferOffset = _serializer.bool(obj.bool_data, buffer, bufferOffset);
    // Serialize message field [int_data]
    bufferOffset = _serializer.int32(obj.int_data, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type BoolStateEyetracking
    let len;
    let data = new BoolStateEyetracking(null);
    // Deserialize message field [bool_data]
    data.bool_data = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [int_data]
    data.int_data = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 5;
  }

  static datatype() {
    // Returns string type for a message object
    return 'Eyetracking/BoolStateEyetracking';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '7718df7148bc03e28cca1a6761586382';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool bool_data
    int32 int_data
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new BoolStateEyetracking(null);
    if (msg.bool_data !== undefined) {
      resolved.bool_data = msg.bool_data;
    }
    else {
      resolved.bool_data = false
    }

    if (msg.int_data !== undefined) {
      resolved.int_data = msg.int_data;
    }
    else {
      resolved.int_data = 0
    }

    return resolved;
    }
};

module.exports = BoolStateEyetracking;
