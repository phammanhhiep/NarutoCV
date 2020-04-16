![alt text](https://github.com/AveryGriffin/NarutoCV/blob/master/extras/mainscreen.PNG)

In this project, I created a Computer Vision based Naruto game.......BELIEVE IT!!!
I wrote a quick blog post about the project on my website https://engineeringsapien.com/narutocv-blog. You can learn more about it there. 

<p>&nbsp
</p>

The aim was to bring the Naruto world to life. Namely, I trained a Convolutional Neural Network to recognize Naruto hand signs.

From there, I recreated a simplied version of the classic Naruto Arena game that incorporated the hand recognition model. The result: a game where you 'attack' by preforming Naruto-style hand signs to activate jutsus!

Currently, the only way to play it is to download the code from my github here. I have instructions for doing so on the blog post.

<p>&nbsp</p>

Disclaimer:
There are several parties for which I owe much credit to:

Naruto-Arena - The whole game idea was pretty much just a copy of Naruto Arena. So I owe the creators of that gem a big thank you. In fact, most of the character icons and attack icons I used in the game I got from their website. Here is the OG Naruto Arena https://naruto-arena.net/

VGG16 - This is the deep learning model I used in this project. It is a model by K. Simonyan and A. Zisserman. Here is their paper https://arxiv.org/abs/1409.1556

Brenner Heintz - A major help was Brenner Heintz. For a while, I struggled to get the model to learn anything and it wasn't until I came across Brenner's article (https://towardsdatascience.com/training-a-neural-network-to-detect-gestures-with-opencv-in-python-e09b0a12bdf1) did things start to come together. It was Brenner who convinced me to use the VGG16 model as well as thresholded images instead of colored images.

The Internet - And of course, I must give a big thanks to the countless number of people on StackOverflow, Youtube, and the internet as a whole who provided the knowledge (and tutorials) to do half the things I tried doing (let's be honest....SO is the author of this project).

Masashi Kishimoto - It goes without saying but the holders of the copyrighted and/or trademarked material appearing in this project belong to NARUTO © 2002 MASASHI KISHIMOTO. All Rights Reserved.
