;; Auto-generated. Do not edit!


(when (boundp 'Eyetracking::BoolState)
  (if (not (find-package "EYETRACKING"))
    (make-package "EYETRACKING"))
  (shadow 'BoolState (find-package "EYETRACKING")))
(unless (find-package "EYETRACKING::BOOLSTATE")
  (make-package "EYETRACKING::BOOLSTATE"))

(in-package "ROS")
;;//! \htmlinclude BoolState.msg.html


(defclass Eyetracking::BoolState
  :super ros::object
  :slots (_bool_data _int_data ))

(defmethod Eyetracking::BoolState
  (:init
   (&key
    ((:bool_data __bool_data) nil)
    ((:int_data __int_data) 0)
    )
   (send-super :init)
   (setq _bool_data __bool_data)
   (setq _int_data (round __int_data))
   self)
  (:bool_data
   (&optional (__bool_data :null))
   (if (not (eq __bool_data :null)) (setq _bool_data __bool_data)) _bool_data)
  (:int_data
   (&optional __int_data)
   (if __int_data (setq _int_data __int_data)) _int_data)
  (:serialization-length
   ()
   (+
    ;; bool _bool_data
    1
    ;; int32 _int_data
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _bool_data
       (if _bool_data (write-byte -1 s) (write-byte 0 s))
     ;; int32 _int_data
       (write-long _int_data s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _bool_data
     (setq _bool_data (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; int32 _int_data
     (setq _int_data (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get Eyetracking::BoolState :md5sum-) "7718df7148bc03e28cca1a6761586382")
(setf (get Eyetracking::BoolState :datatype-) "Eyetracking/BoolState")
(setf (get Eyetracking::BoolState :definition-)
      "bool bool_data
int32 int_data
")



(provide :Eyetracking/BoolState "7718df7148bc03e28cca1a6761586382")


