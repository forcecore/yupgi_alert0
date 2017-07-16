; clips AI rules for Yupgi Alert

; Age of Kings use rule based AI so...
; I think that will be helpful.

; To build buildings:
; Assert
; (make name priority)
; To train units:
; Assert
; (train name priority)

(deftemplate can-make
    (slot name)
)

(deftemplate make
    (slot name)
    (slot priority (default 1))
)

(deftemplate actor-type-count
    (slot name)
    (slot count)
)

(deftemplate surplus-power
    (slot amount)
)

(deftemplate need-power
    (slot amount)
)

(deffunction clear-stuff ()
    (do-for-all-facts
        ((?fact can-make)) TRUE
            (retract ?fact))
    (do-for-all-facts
        ((?fact actor-type-count)) TRUE
            (retract ?fact))
    (do-for-all-facts
        ((?fact make)) TRUE
            (retract ?fact))
    (do-for-all-facts
        ((?fact surplus-power)) TRUE
            (retract ?fact))
    (do-for-all-facts
        ((?fact need-power)) TRUE
            (retract ?fact))
)

(deffacts master-strategy
    (strategy-early-tank-rush 0)
    (strategy-early-inf-rush 0)
    (strategy-artillary-rush 0)
    (strategy-air-support 0)
    (strategy-harv-harrass 0)
    (strategy-mcv-push 0)
)

(deffacts ai-params
    (param-power-surplus 100)
)

(defrule harvester-rule
    (can-make (name harv))
    (actor-type-count (name harv) (count ?num))
    (test (< ?num 5))
=>
    (assert (make (name harv) (priority 10)))
)

; rule to make extra powerplants
(defrule surplus-powerplants
    (can-make (name power))
    (surplus-power (amount ?sp))
    (param-power-surplus ?paramSP)
    (test (< ?sp ?paramSP))
=>
    (assert (make (name power) (priority 1)))
)

; rule to escape low power
(defrule in-low-power
    (can-make (name power))
    (surplus-power (amount ?sp))
    (test (< ?sp 0))
=>
    (assert (make (name power) (priority 20)))
)

; translate can make {apwr,powr} to can-make power.
(defrule can-make-powr
    (can-make (name powr))
=>
    (assert (can-make (name power)))
)
(defrule can-make-apwr
    (can-make (name apwr))
=>
    (assert (can-make (name power)))
)

(defrule make-needed-power
    (can-make (name power))
    (make (name ?buildingName) (priority ?priority))
    (need-power (amount ?requiredPowerAmount))
    (surplus-power (amount ?sp))
    (test (< ?sp ?requiredPowerAmount))
=>
    (assert (make (name power) (priority 20)))
)

; translate power to powr or apwr
(defrule make-best-power-powr
    (declare (salience 5))

    (make (name power) (priority ?p))
    (can-make (name powr))
=>
    (assert (make (name powr) (priority ?p)))
)
; translate power to powr or apwr
(defrule make-best-power-apwr
    (declare (salience 5))

    (make (name power) (priority ?p))
    (can-make (name apwr))
=>
    (assert (make (name apwr) (priority ?p)))
)

; make proc
(defrule make-proc
    (declare (salience 10))

    (can-make (name proc))
    (actor-type-count (name proc) (count ?n))
    (test (< ?n 4))
=>
    (assert (make (name proc) (priority 10)))
    (assert (need-power (amount 30)))
)

; (reset) ; needed after load!
(deffacts test
     (surplus-power (amount -1))
     (can-make (name proc))
     (can-make (name apwr))
     (can-make (name powr))
     (can-make (name harv))
     (actor-type-count (name harv) (count 2))
     (actor-type-count (name proc) (count 2))
)
