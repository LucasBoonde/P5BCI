;; Auto-generated. Do not edit!


(when (boundp 'BCI::BoolStateBCI)
  (if (not (find-package "BCI"))
    (make-package "BCI"))
  (shadow 'BoolStateBCI (find-package "BCI")))
(unless (find-package "BCI::BOOLSTATEBCI")
  (make-package "BCI::BOOLSTATEBCI"))

(in-package "ROS")
;;//! \htmlinclude BoolStateBCI.msg.html


(defclass BCI::BoolStateBCI
  :super ros::object
  :slots (_data ))

(defmethod BCI::BoolStateBCI
  (:init
   (&key
    ((:data __data) nil)
    )
   (send-super :init)
   (setq _data __data)
   self)
  (:data
   (&optional (__data :null))
   (if (not (eq __data :null)) (setq _data __data)) _data)
  (:serialization-length
   ()
   (+
    ;; bool _data
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _data
       (if _data (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _data
     (setq _data (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(setf (get BCI::BoolStateBCI :md5sum-) "8b94c1b53db61fb6aed406028ad6332a")
(setf (get BCI::BoolStateBCI :datatype-) "BCI/BoolStateBCI")
(setf (get BCI::BoolStateBCI :definition-)
      "bool data
")



(provide :BCI/BoolStateBCI "8b94c1b53db61fb6aed406028ad6332a")


