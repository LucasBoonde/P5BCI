
(cl:in-package :asdf)

(defsystem "BCI-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "BoolStateBCI" :depends-on ("_package_BoolStateBCI"))
    (:file "_package_BoolStateBCI" :depends-on ("_package"))
  ))