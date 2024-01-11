; Auto-generated. Do not edit!


(cl:in-package BCI-msg)


;//! \htmlinclude BoolState.msg.html

(cl:defclass <BoolState> (roslisp-msg-protocol:ros-message)
  ((data
    :reader data
    :initarg :data
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass BoolState (<BoolState>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <BoolState>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'BoolState)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name BCI-msg:<BoolState> is deprecated: use BCI-msg:BoolState instead.")))

(cl:ensure-generic-function 'data-val :lambda-list '(m))
(cl:defmethod data-val ((m <BoolState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader BCI-msg:data-val is deprecated.  Use BCI-msg:data instead.")
  (data m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <BoolState>) ostream)
  "Serializes a message object of type '<BoolState>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'data) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <BoolState>) istream)
  "Deserializes a message object of type '<BoolState>"
    (cl:setf (cl:slot-value msg 'data) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<BoolState>)))
  "Returns string type for a message object of type '<BoolState>"
  "BCI/BoolState")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'BoolState)))
  "Returns string type for a message object of type 'BoolState"
  "BCI/BoolState")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<BoolState>)))
  "Returns md5sum for a message object of type '<BoolState>"
  "8b94c1b53db61fb6aed406028ad6332a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'BoolState)))
  "Returns md5sum for a message object of type 'BoolState"
  "8b94c1b53db61fb6aed406028ad6332a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<BoolState>)))
  "Returns full string definition for message of type '<BoolState>"
  (cl:format cl:nil "bool data~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'BoolState)))
  "Returns full string definition for message of type 'BoolState"
  (cl:format cl:nil "bool data~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <BoolState>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <BoolState>))
  "Converts a ROS message object to a list"
  (cl:list 'BoolState
    (cl:cons ':data (data msg))
))
