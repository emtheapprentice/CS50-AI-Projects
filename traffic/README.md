# Traffic.py
### Video Demo: 
<https://youtu.be/yI-zRYtKAls>
### Experimentation process:
I first tried the structure used in handwriting.py and found out it worked terribly here.
Then I tried adding more hidden layers, neurons and playing with dropout and that wasn't
improving things either. I did the convolutional and pooling steps twice like Brian 
mentioned, but figured the images were already pixellated enough for pooling twice
and indeed I found out that pooling once and for no more than 2x2 pixels worked best.
When I finally thought about inserting more convolutional layers, the accuracy improved
dramatically and I found that was the key. I experimented some more with dropout and
also found out it worked better with a low amount, especially in the last layer.