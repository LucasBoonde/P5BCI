
(cl:in-package :asdf)

(defsystem "Eyetracking-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "BoolStateEyetracking" :depends-on ("_package_BoolStateEyetracking"))
    (:file "_package_BoolStateEyetracking" :depends-on ("_package"))
  ))