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

; count the AI's actors
(deftemplate actor-type-count
    (slot name)
    (slot count)
)

; enemy has these
(deftemplate enemy-has
    (slot name)
    (slot count)
)

(deftemplate excess-power
    (slot amount)
)

(deftemplate need-power
    (slot amount)
)

(deffunction get-make-list ()
    (bind ?facts (find-all-facts ((?f make)) True))
    (sort sort-make ?facts)
)

(deffunction sort-make (?m1 ?m2)
   (< (fact-slot-value ?m1 priority)
      (fact-slot-value ?m2 priority)))

(deffunction get-actor-type-count (?name)
    (bind ?facts (find-fact ((?f actor-type-count)) (eq ?f:name ?name)))
    (if (= (length$ ?facts) 0)
    then
        0
    else
        (fact-slot-value (nth$ 1 ?facts) count))
)

(deffunction update-actor-type-count (?name ?count)
    (bind ?facts (find-fact ((?f actor-type-count)) (eq ?f:name ?name)))
    (if (= (length$ ?facts) 0)
    then
        (assert (actor-type-count (name ?name) (count ?count)))
    else
        (bind ?fact (nth$ 1 ?facts))
        (modify ?fact (count ?count))
    )
)

(deffunction update-excess-power (?amount)
    (bind ?facts (find-fact ((?f excess-power)) TRUE))
    (if (eq (length$ ?facts) 0)
    then
        (assert (excess-power (amount ?amount)))
    else
        (bind ?fact (nth$ 1 ?facts))
        (modify ?fact (amount ?amount))
    )
)

(deffunction enable-can-make (?name)
    (bind ?facts (find-fact ((?f can-make)) (eq ?f:name ?name)))
    (if (= (length$ ?facts) 0)
    then
        (assert (can-make (name ?name))))
)

(deffunction disable-can-make (?name)
    (bind ?facts (find-fact ((?f can-make)) (eq ?f:name ?name)))
    (if (<> (length$ ?facts) 0)
    then
        (bind ?fact (nth$ 1 ?facts))
        ;(retract ?fact)
    )
)

;-------------------------------------------------------------------------------
; Power stuff
;-------------------------------------------------------------------------------

(deffacts master-strategy
    (strategy-early-tank-rush 0)
    (strategy-early-inf-rush 0)
    (strategy-artillary-rush 0)
    (strategy-air-support 0)
    (strategy-harv-harrass 0)
    (strategy-mcv-push 0)
)

(deffacts ai-params
    (param-power-excess 0)
)

;-------------------------------------------------------------------------------
; Power stuff
;-------------------------------------------------------------------------------

; Required amount of power rule...
; These are automatically fed from the AI now.
; But I left these as a comment so that you can see how things are going on.
;
;(defrule power-req-proc
;    (make (name proc))
;=>
;    (assert (need-power (amount 30)))
;)
;(defrule power-req-tent
;    (make (name tent))
;=>
;    (assert (need-power (amount 20)))
;)

; rule to make extra powerplants
(defrule excess-powerplants
    (can-make (name power))
    (excess-power (amount ?ep))
    (param-power-excess ?paramEP)
    (test (< ?ep ?paramEP))
=>
    (assert (make (name power) (priority 1)))
)

; rule to escape low power
(defrule in-low-power
    (can-make (name power))
    (excess-power (amount ?ep))
    (test (< ?ep 0))
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
    (excess-power (amount ?ep))
    (test (< ?ep ?requiredPowerAmount))
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

;-------------------------------------------------------------------------------
; Build order related stuff
;-------------------------------------------------------------------------------

; Any human (non-ant) build order starts from here!
(defrule make-proc
    (declare (salience 10))

    ; deduces powerplant automatically using power requirements!
    ;(can-make (name proc))
    (test (< (get-actor-type-count proc) 4))
=>
    (assert (make (name proc) (priority 10)))
)

(defrule make-tent
    (declare (salience 10))

    (can-make (name tent))
    (test (< (get-actor-type-count tent) 1))
=>
    (assert (make (name tent) (priority 40)))
)

(defrule make-barr
    (declare (salience 10))

    (can-make (name barr))
    (test (< (get-actor-type-count barr) 1))
=>
    (assert (make (name barr) (priority 40)))
)

(defrule make-gaweap
    (declare (salience 10))

    (can-make (name gaweap))
    (test (< (get-actor-type-count gaweap) 1))
=>
    (assert (make (name gaweap) (priority 30)))
)

(defrule make-naweap
    (declare (salience 10))

    (can-make (name naweap))
    (test (< (get-actor-type-count naweap) 1))
=>
    (assert (make (name naweap) (priority 30)))
)

;-------------------------------------------------------------------------------
; Unit building rules
;-------------------------------------------------------------------------------

(defrule harvester-rule
    (can-make (name harv))
    (test (< (get-actor-type-count harv) 1))
=>
    (assert (make (name harv) (priority 10)))
)

;-------------------------------------------------------------------------------
; Test facts
;-------------------------------------------------------------------------------

; (reset) ; needed after load!
;(deffacts test
;     (excess-power (amount 1000))
;     (can-make (name proc))
;     (can-make (name apwr))
;     (can-make (name powr))
;     (can-make (name harv))
;     (actor-type-count (name harv) (count 2))
;     (actor-type-count (name proc) (count 2))
;)
