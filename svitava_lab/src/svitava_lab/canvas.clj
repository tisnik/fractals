(ns svitava-lab.canvas)

(defn create
  "Create new canvas."
  [title width height]
  (let [frame    (new javax.swing.JFrame title)
        panel    (.getContentPane frame)
        size     (new java.awt.Dimension width height)]
    (.setPreferredSize panel size)
    (.setBackground panel java.awt.Color/white)
    (.pack frame)
    {:frame    frame
     :panel    panel
     :graphics (.getGraphics panel)}))

(defn open
  "Open new canvas on screen."
  [title width height]
  (let [canvas (create title width height)]
    (.setVisible (:frame canvas) true)
    canvas))

(defn clear!
  "Clear the canvas."
  [canvas]
  (let [panel    (:panel canvas)
        graphics (:graphics canvas)]
      (.setBackground panel (.getBackground panel))
      (.clearRect graphics 0 0 (.getWidth panel) (.getHeight panel))))

(defn close!
  "Close the canvas."
  [canvas]
  (let [frame (:frame canvas)]
    (doto frame
      (.setVisible false)
      (.dispose))))

(defn set-color!
  "Set drawing color."
  [canvas color]
  (let [graphics (:graphics canvas)]
    (.setColor graphics color)))

(defn draw!
  "Draw a line onto canvas."
  [canvas x1 y1 x2 y2]
  (let [graphics (:graphics canvas)]
    (.drawLine graphics x1 y1 x2 y2)))

(defn bitblt!
  "Draw a bitmap onto canvas."
  [canvas bitmap x y]
  (let [graphics (:graphics canvas)]
    (.drawImage graphics bitmap x y nil)))

(comment
  ;; example of use

(require '[svitava-lab.canvas :as canvas])
(require '[svitava-lab.bitmap :as bitmap])

(let [c (canvas/open "foo" 640 480)
      b (bitmap/create 640 480)]
  (bitmap/putpixel b 100 100 0x00 0x00 0xff)
  (bitmap/putpixel b 101 100 0x00 0x00 0xff)
  (bitmap/putpixel b 101 101 0x00 0x00 0xff)
  (bitmap/putpixel b 100 101 0x00 0x00 0xff)
  (canvas/clear! c)
  (java.lang.Thread/sleep 1000)
  (canvas/draw! c 0 0 640 480)
  (canvas/bitblt! c b 0 0)
  (java.lang.Thread/sleep 1000)
  (canvas/close! c)
  (java.lang.Thread/sleep 1000))

(let [c (open "foo" 640 480)]
  (clear! c)
  (java.lang.Thread/sleep 1000)
  (draw! c 0 0 640 480)
  (java.lang.Thread/sleep 1000)
  (close! c)
  (java.lang.Thread/sleep 1000))

)
