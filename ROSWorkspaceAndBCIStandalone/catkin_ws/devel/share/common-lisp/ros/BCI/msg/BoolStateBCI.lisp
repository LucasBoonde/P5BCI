; Auto-generated. Do not edit!


(cl:in-package BCI-msg)


;//! \htmlinclude BoolStateBCI.msg.html

(cl:defclass <BoolStateBCI> (roslisp-msg-protocol:ros-message)
  ((data
    :reader data
    :initarg :data
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass BoolStateBCI (<BoolStateBCI>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <BoolStateBCI>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'BoolStateBCI)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name BCI-msg:<BoolStateBCI> is deprecated: use BCI-msg:BoolStateBCI instead.")))

(cl:ensure-generic-function 'data-val :lambda-list '(m))
(cl:defmethod data-val ((m <BoolStateBCI>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader BCI-msg:data-val is deprecated.  Use BCI-msg:data instead.")
  (data m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <BoolStateBCI>) ostream)
  "Serializes a message object of type '<BoolStateBCI>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'data) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <BoolStateBCI>) istream)
  "Deserializes a message object of type '<BoolStateBCI>"
    (cl:setf (cl:slot-value msg 'data) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<BoolStateBCI>)))
  "Returns string type for a message object of type '<BoolStateBCI>"
  "BCI/BoolStateBCI")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'BoolStateBCI)))
  "Returns string type for a message object of type 'BoolStateBCI"
  "BCI/BoolStateBCI")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<BoolStateBCI>)))
  "Returns md5sum for a message object of type '<BoolStateBCI>"
  "8b94c1b53db61fb6aed406028ad6332a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'BoolStateBCI)))
  "Returns md5sum for a message object of type 'BoolStateBCI"
  "8b94c1b53db61fb6aed406028ad6332a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<BoolStateBCI>)))
  "Returns full string definition for message of type '<BoolStateBCI>"
  (cl:format cl:nil "bool data~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'BoolStateBCI)))
  "Returns full string definition for message of type 'BoolStateBCI"
  (cl:format cl:nil "bool data~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <BoolStateBCI>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <BoolStateBCI>))
  "Converts a ROS message object to a list"
  (cl:list 'BoolStateBCI
    (cl:cons ':data (data msg))
))
