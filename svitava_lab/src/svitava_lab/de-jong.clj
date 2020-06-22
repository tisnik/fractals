(ns svitava-lab.de-jong)

(require '[svitava-lab.canvas :as canvas])
(require '[svitava-lab.bitmap :as bitmap])

(defn de-jong-attractor-iter
  "De-Jong attractor."
  [a b c d [x y]]
  [(- (Math/sin (* a y))
      (Math/cos (* b x)))
   (- (Math/sin (* c x))
      (Math/cos (* d y)))])

; a, b, c, d in range -pi..pi

(let [c (canvas/open "foo" 640 480)
      b (bitmap/create 640 480)
      n 500000
      settle-down 1000
      A -2.7
      B -0.09
      C -0.86
      D -2.20
      x 0.0
      y 0.0]
  (loop [x 0.0
         y 0.0
         i 0]
    (when (< i n)
      ;(println x y)
      (if (> i settle-down)
        (bitmap/putpixel b (+ 400 (* x 120)) (+ 240 (* y 120)) 0xff 0xff 0xff))
      (let [[xn yn] (de-jong-attractor-iter A B C D [x y])]
      (recur xn yn (inc i)))))
  (canvas/clear! c)
  (java.lang.Thread/sleep 100)
  (canvas/bitblt! c b 0 0)
  (java.lang.Thread/sleep 2000)
  (canvas/close! c)
  (java.lang.Thread/sleep 100))
