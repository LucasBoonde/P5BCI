; Auto-generated. Do not edit!


(cl:in-package Eyetracking-msg)


;//! \htmlinclude BoolState.msg.html

(cl:defclass <BoolState> (roslisp-msg-protocol:ros-message)
  ((bool_data
    :reader bool_data
    :initarg :bool_data
    :type cl:boolean
    :initform cl:nil)
   (int_data
    :reader int_data
    :initarg :int_data
    :type cl:integer
    :initform 0))
)

(cl:defclass BoolState (<BoolState>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <BoolState>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'BoolState)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name Eyetracking-msg:<BoolState> is deprecated: use Eyetracking-msg:BoolState instead.")))

(cl:ensure-generic-function 'bool_data-val :lambda-list '(m))
(cl:defmethod bool_data-val ((m <BoolState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader Eyetracking-msg:bool_data-val is deprecated.  Use Eyetracking-msg:bool_data instead.")
  (bool_data m))

(cl:ensure-generic-function 'int_data-val :lambda-list '(m))
(cl:defmethod int_data-val ((m <BoolState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader Eyetracking-msg:int_data-val is deprecated.  Use Eyetracking-msg:int_data instead.")
  (int_data m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <BoolState>) ostream)
  "Serializes a message object of type '<BoolState>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'bool_data) 1 0)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'int_data)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <BoolState>) istream)
  "Deserializes a message object of type '<BoolState>"
    (cl:setf (cl:slot-value msg 'bool_data) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'int_data) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<BoolState>)))
  "Returns string type for a message object of type '<BoolState>"
  "Eyetracking/BoolState")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'BoolState)))
  "Returns string type for a message object of type 'BoolState"
  "Eyetracking/BoolState")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<BoolState>)))
  "Returns md5sum for a message object of type '<BoolState>"
  "7718df7148bc03e28cca1a6761586382")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'BoolState)))
  "Returns md5sum for a message object of type 'BoolState"
  "7718df7148bc03e28cca1a6761586382")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<BoolState>)))
  "Returns full string definition for message of type '<BoolState>"
  (cl:format cl:nil "bool bool_data~%int32 int_data~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'BoolState)))
  "Returns full string definition for message of type 'BoolState"
  (cl:format cl:nil "bool bool_data~%int32 int_data~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <BoolState>))
  (cl:+ 0
     1
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <BoolState>))
  "Converts a ROS message object to a list"
  (cl:list 'BoolState
    (cl:cons ':bool_data (bool_data msg))
    (cl:cons ':int_data (int_data msg))
))
