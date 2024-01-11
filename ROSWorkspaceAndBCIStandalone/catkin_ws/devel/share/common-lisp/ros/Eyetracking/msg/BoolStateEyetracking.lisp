; Auto-generated. Do not edit!


(cl:in-package Eyetracking-msg)


;//! \htmlinclude BoolStateEyetracking.msg.html

(cl:defclass <BoolStateEyetracking> (roslisp-msg-protocol:ros-message)
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

(cl:defclass BoolStateEyetracking (<BoolStateEyetracking>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <BoolStateEyetracking>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'BoolStateEyetracking)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name Eyetracking-msg:<BoolStateEyetracking> is deprecated: use Eyetracking-msg:BoolStateEyetracking instead.")))

(cl:ensure-generic-function 'bool_data-val :lambda-list '(m))
(cl:defmethod bool_data-val ((m <BoolStateEyetracking>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader Eyetracking-msg:bool_data-val is deprecated.  Use Eyetracking-msg:bool_data instead.")
  (bool_data m))

(cl:ensure-generic-function 'int_data-val :lambda-list '(m))
(cl:defmethod int_data-val ((m <BoolStateEyetracking>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader Eyetracking-msg:int_data-val is deprecated.  Use Eyetracking-msg:int_data instead.")
  (int_data m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <BoolStateEyetracking>) ostream)
  "Serializes a message object of type '<BoolStateEyetracking>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'bool_data) 1 0)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'int_data)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <BoolStateEyetracking>) istream)
  "Deserializes a message object of type '<BoolStateEyetracking>"
    (cl:setf (cl:slot-value msg 'bool_data) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'int_data) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<BoolStateEyetracking>)))
  "Returns string type for a message object of type '<BoolStateEyetracking>"
  "Eyetracking/BoolStateEyetracking")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'BoolStateEyetracking)))
  "Returns string type for a message object of type 'BoolStateEyetracking"
  "Eyetracking/BoolStateEyetracking")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<BoolStateEyetracking>)))
  "Returns md5sum for a message object of type '<BoolStateEyetracking>"
  "7718df7148bc03e28cca1a6761586382")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'BoolStateEyetracking)))
  "Returns md5sum for a message object of type 'BoolStateEyetracking"
  "7718df7148bc03e28cca1a6761586382")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<BoolStateEyetracking>)))
  "Returns full string definition for message of type '<BoolStateEyetracking>"
  (cl:format cl:nil "bool bool_data~%int32 int_data~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'BoolStateEyetracking)))
  "Returns full string definition for message of type 'BoolStateEyetracking"
  (cl:format cl:nil "bool bool_data~%int32 int_data~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <BoolStateEyetracking>))
  (cl:+ 0
     1
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <BoolStateEyetracking>))
  "Converts a ROS message object to a list"
  (cl:list 'BoolStateEyetracking
    (cl:cons ':bool_data (bool_data msg))
    (cl:cons ':int_data (int_data msg))
))
