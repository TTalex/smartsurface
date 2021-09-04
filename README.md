This project aims at converting any surface (wall, desk) into a smart surface.

It uses four aruco tags to define the bounds of a given surface and a fifth one as a cursor. The tags are tracked in real time using a webcam.

An Mqtt server is used to broadcast the significant changes in the cursor position.

Applications can then sub to the updates and act accordingly.
