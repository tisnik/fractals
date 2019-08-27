#mencoder mf://*.png -mf w=800:h=600:fps=16:type=png -ovc lavc \
    vcodec=mpeg4:tsaf:vbitrate=24000 -oac copy -o output.avi -nosound

mencoder mf://*.png -mf w=800:h=600:fps=16:type=png -o output.avi -ovc xvid -xvidencopts pass=2:bitrate=3000

#mencoder mf://*.png -mf w=800:h=600:fps=16:type=png -o output.avi -ovc xvid -xvidencopts pass=2:bitrate=2000
